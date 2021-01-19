# Copyright (C) 2006-2021 by the Free Software Foundation, Inc.
#
# This file is part of GNU Mailman.
#
# GNU Mailman is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# GNU Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Mailman.  If not, see <https://www.gnu.org/licenses/>.

"""Configuration file loading and management."""

import os
import sys
import mailman.templates

from configparser import ConfigParser
from contextlib import ExitStack
from flufl.lock import Lock
from importlib_resources import path, read_text
from lazr.config import ConfigSchema, as_boolean
from mailman import version
from mailman.interfaces.configuration import (
    ConfigurationUpdatedEvent, IConfiguration, MissingConfigurationFileError)
from mailman.interfaces.languages import ILanguageManager
from mailman.utilities.filesystem import makedirs
from mailman.utilities.modules import call_name, expand_path
from public import public
from string import Template
from zope.component import getUtility
from zope.event import notify
from zope.interface import implementer


SPACE = ' '
SPACERS = '\n'
DIR_NAMES = (
    'archive',
    'bin',
    'cache',
    'data',
    'etc',
    'list_data',
    'lock',
    'log',
    'messages',
    'queue',
    )


MAILMAN_CFG_TEMPLATE = """\
# AUTOMATICALLY GENERATED BY MAILMAN ON {} UTC
#
# This is your GNU Mailman 3 configuration file.  You can edit this file to
# configure Mailman to your needs, and Mailman will never overwrite it.
# Additional configuration information is available here:
#
# https://mailman.readthedocs.io/en/latest/src/mailman/config/docs/config.html
#
# For example, uncomment the following lines to run Mailman in developer mode.
#
# [devmode]
# enabled: yes
# recipient: your.address@your.domain"""


@public
class ARC:
    """ARC represents the parameters required for validation of arc."""
    # This is a perfect candidate for dataclass when we are ready to support
    # Python 3.7+. This class is a namespace to store the ARC related params in
    # a single namespace.
    authserv_id = None
    trusted_authserv_ids = None
    private_key = None
    arc_headers = None
    selector = None
    domain = None
    dkim_enabled = False
    dmarc_enabled = False


@public
@implementer(IConfiguration)
class Configuration:
    """The core global configuration object."""

    def __init__(self):
        self.switchboards = {}
        self.QFILE_SCHEMA_VERSION = version.QFILE_SCHEMA_VERSION
        self._config = None
        self.filename = None
        # Whether to create run-time paths or not.  This is for the test
        # suite, which will set this to False until the test layer is set up.
        self.create_paths = True
        # Create various registries.
        self.chains = {}
        self.rules = {}
        self.handlers = {}
        self.pipelines = {}
        self.commands = {}
        self.plugins = {}
        self.password_context = None
        self.db = None
        # ARC parameters.
        self.arc_enabled = False
        self.arc = ARC()

    def _clear(self):
        """Clear the cached configuration variables."""
        self.switchboards.clear()
        getUtility(ILanguageManager).clear()

    def __getattr__(self, name):
        """Delegate to the configuration object."""
        return getattr(self._config, name)

    def __iter__(self):
        return iter(self._config)

    def load(self, filename=None):
        """Load the configuration from the schema and config files."""
        with path('mailman.config', 'schema.cfg') as schema_file:
            schema = ConfigSchema(str(schema_file))
        # If a configuration file was given, load it now too.  First, load
        # the absolute minimum default configuration, then if a
        # configuration filename was given by the user, push it.
        with path('mailman.config', 'mailman.cfg') as config_path:
            self._config = schema.load(str(config_path))
        if filename is None:
            self._post_process()
        else:
            self.filename = filename
            with open(filename, 'r', encoding='utf-8') as user_config:
                self.push(filename, user_config.read())

    def push(self, config_name, config_string):
        """Push a new configuration onto the stack."""
        self._clear()
        self._config.push(config_name, config_string)
        self._post_process()

    def pop(self, config_name):
        """Pop a configuration from the stack."""
        self._clear()
        self._config.pop(config_name)
        self._post_process()

    def _post_process(self):
        """Perform post-processing after loading the configuration files."""
        # Expand and set up all directories.
        self._expand_paths()
        self.ensure_directories_exist()
        self._update_arc_parameters()
        notify(ConfigurationUpdatedEvent(self))

    def _expand_paths(self):
        """Expand all configuration paths."""
        # Set up directories.
        default_bin_dir = os.path.abspath(os.path.dirname(sys.executable))
        # Now that we've loaded all the configuration files we're going to
        # load, set up some useful directories based on the settings in the
        # configuration file.
        layout = 'paths.' + self._config.mailman.layout
        for category in self._config.getByCategory('paths'):
            if category.name == layout:
                break
        else:
            print('No path configuration found:', layout, file=sys.stderr)
            sys.exit(1)
        # First, collect all variables in a substitution dictionary.  $VAR_DIR
        # is taken from the environment or from the configuration file if the
        # environment is not set.  Because the var_dir setting in the config
        # file could be a relative path, and because 'mailman start' chdirs to
        # $VAR_DIR, without this subprocesses bin/master and bin/runner will
        # create $VAR_DIR hierarchies under $VAR_DIR when that path is
        # relative.
        var_dir = os.environ.get('MAILMAN_VAR_DIR', category.var_dir)
        substitutions = dict(
            cwd=os.getcwd(),
            argv=default_bin_dir,
            var_dir=var_dir,
            template_dir=(
                os.path.dirname(mailman.templates.__file__)
                if category.template_dir == ':source:'
                else category.template_dir),
            )
        # Directories.
        for name in DIR_NAMES:
            key = '{}_dir'.format(name)
            substitutions[key] = getattr(category, key)
        # Files.
        for name in ('lock', 'pid'):
            key = '{}_file'.format(name)
            substitutions[key] = getattr(category, key)
        # Add the path to the .cfg file, if one was given on the command line.
        if self.filename is not None:
            substitutions['cfg_file'] = self.filename
        # Now, perform substitutions recursively until there are no more
        # variables with $-vars in them, or until substitutions are not
        # helping any more.
        last_dollar_count = 0
        while True:
            expandables = []
            # Mutate the dictionary during iteration.
            for key in substitutions:
                raw_value = substitutions[key]
                value = Template(raw_value).safe_substitute(substitutions)
                if '$' in value:
                    # Still more work to do.
                    expandables.append((key, value))
                substitutions[key] = value
            if len(expandables) == 0:
                break
            if len(expandables) == last_dollar_count:
                print('Path expansion infloop detected:\n',
                      SPACERS.join('\t{}: {}'.format(key, value)
                                   for key, value in sorted(expandables)),
                      file=sys.stderr)
                sys.exit(1)
            last_dollar_count = len(expandables)
        # Ensure that all paths are normalized and made absolute.  Handle the
        # few special cases first.  Most of these are due to backward
        # compatibility.
        self.PID_FILE = os.path.abspath(substitutions.pop('pid_file'))
        for key in substitutions:
            attribute = key.upper()
            setattr(self, attribute, os.path.abspath(substitutions[key]))

    @property
    def logger_configs(self):
        """Return all log config sections."""
        return self._config.getByCategory('logging', [])

    @property
    def paths(self):
        """Return a substitution dictionary of all path variables."""
        return dict((k, self.__dict__[k])
                    for k in self.__dict__
                    if k.endswith('_DIR'))

    def ensure_directories_exist(self):
        """Create all path directories if they do not exist."""
        if self.create_paths:
            for variable, directory in self.paths.items():
                makedirs(directory)
            # Avoid circular imports.
            from mailman.utilities.datetime import now
            # Create a mailman.cfg template file if it doesn't already exist.
            # LBYL: <boo hiss>, but it's probably okay because the directories
            # likely didn't exist before the above loop, and we'll create a
            # temporary lock.
            lock_file = os.path.join(self.LOCK_DIR, 'mailman-cfg.lck')
            mailman_cfg = os.path.join(self.ETC_DIR, 'mailman.cfg')
            with Lock(lock_file):
                if not os.path.exists(mailman_cfg):
                    with open(mailman_cfg, 'w') as fp:
                        print(MAILMAN_CFG_TEMPLATE.format(
                            now().replace(microsecond=0)), file=fp)

    @property
    def runner_configs(self):
        """Iterate over all the runner configuration sections."""
        yield from self._config.getByCategory('runner', [])

    @property
    def archivers(self):
        """Iterate over all the archivers."""
        for section in self._config.getByCategory('archiver', []):
            class_path = section['class'].strip()
            if len(class_path) == 0:
                continue
            archiver = call_name(class_path)
            archiver.is_enabled = as_boolean(section.enable)
            yield archiver

    @property
    def plugin_configs(self):
        """Return all the plugin configuration sections."""
        plugin_sections = self._config.getByCategory('plugin', [])
        for section in plugin_sections:
            # 2017-08-27 barry: There's a fundamental constraint imposed by
            # lazr.config, namely that we have to use a .master section instead
            # of a .template section in the schema.cfg, or user supplied
            # configuration files cannot define new [plugin.*] sections.  See
            # https://bugs.launchpad.net/lazr.config/+bug/310619 for
            # additional details.
            #
            # However, this means that [plugin.master] will show up in the
            # categories retrieved above.  But 'master' is not a real plugin,
            # so we need to skip it (e.g. otherwise we'll get log warnings
            # about plugin.master being disabled, etc.).  This imposes an
            # additional limitation though in that users cannot define a
            # plugin named 'master' because you can't override a master
            # section with a real section.  There's no good way around this so
            # we just have to live with this limitation.
            if section.name == 'plugin.master':
                continue
            # The section.name will be something like 'plugin.example', but we
            # only want the 'example' part as the name of the plugin.  We
            # could split on dots, but lazr.config gives us a different way.
            # `category_and_section_names` is a 2-tuple of e.g.
            # ('plugin', 'example'), so just grab the last element.
            yield section.category_and_section_names[1], section

    @property
    def language_configs(self):
        """Iterate over all the language configuration sections."""
        yield from self._config.getByCategory('language', [])

    def _update_arc_parameters(self):
        """Update ARC related parameters by loading them from new config."""

        self.arc_enabled = self.ARC.enabled.strip().lower() == 'yes'
        # Load the private key to sign the messages.
        if self.arc_enabled:
            ids = self.ARC.trusted_authserv_ids.split(',')
            ids.append(self.ARC.authserv_id)
            self.arc.trusted_authserv_ids = [x.strip() for x in ids]
            # The list of headers we need to sign for ARC.
            self.arc.headers = [header.strip().lower().encode()
                                for header in self.ARC.sig_headers.split(',')]
            # Make sure the "From" header is included in arc_headers because we
            # are going to fail when trying to sign a message with a
            # DKIM-exception. It is better to fail early.
            if b'from' not in self.arc.headers:
                print('[ARC] "sig_headers" do not include "From" header.',
                      file=sys.stderr)
                sys.exit(1)
            # Make sure the private signing key is configured if ARC is
            # enabled.
            if self.ARC.privkey.strip() == '':
                print('[ARC] "enabled" but "privkey" is not configured.',
                      file=sys.stderr)
                sys.exit(1)
            try:
                # Open the private key in ascii encoding to make sure it
                # doesn't include any non-ascii characters.
                with open(self.ARC.privkey, encoding='ascii') as fd:
                    arc_private_key = fd.read()
            except OSError as e:
                print('[ARC] "privkey" is unreadable: ', str(e),
                      file=sys.stderr)
                sys.exit(1)
            except UnicodeDecodeError:
                print('[ARC] "privkey" contains non-ascii characters.',
                      file=sys.stderr)
                sys.exit(1)

            self.arc.private_key = arc_private_key.encode()
            self.arc.domain = self.ARC.domain.encode()
            self.arc.selector = self.ARC.selector.encode()
            self.arc.authserv_id = self.ARC.authserv_id
            self.arc.dkim_enabled = self.ARC.dkim == 'yes'
            self.arc.dmarc_enabled = self.ARC.dmarc == 'yes'
        else:
            # Reset arc params.
            self.arc = ARC()


@public
def load_external(path):
    """Load the configuration file named by path.

    :param path: A string naming the location of the external configuration
        file.  This is either an absolute file system path or a special
        ``python:`` path.  When path begins with ``python:``, the rest of the
        value must name a ``.cfg`` file located within Python's import path,
        however the trailing ``.cfg`` suffix is implied (don't provide it
        here).
    :return: The contents of the configuration file.
    :rtype: str
    """
    # Is the context coming from a file system or Python path?
    if path.startswith('python:'):
        resource_path = path[7:]
        package, dot, resource = resource_path.rpartition('.')
        return read_text(package, resource + '.cfg')
    with open(path, 'r', encoding='utf-8') as fp:
        return fp.read()


@public
def external_configuration(path):
    """Parse the configuration file named by path.

    :param path: A string naming the location of the external configuration
        file.  This is either an absolute file system path or a special
        ``python:`` path.  When path begins with ``python:``, the rest of the
        value must name a ``.cfg`` file located within Python's import path,
        however the trailing ``.cfg`` suffix is implied (don't provide it
        here).
    :return: A `ConfigParser` instance.
    """
    # Is the context coming from a file system or Python path?
    with ExitStack() as resources:
        cfg_path = str(expand_path(resources, path))
    parser = ConfigParser()
    files = parser.read(cfg_path)
    if files != [cfg_path]:
        raise MissingConfigurationFileError(path)
    return parser
