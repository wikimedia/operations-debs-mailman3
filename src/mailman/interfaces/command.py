# Copyright (C) 2008-2021 by the Free Software Foundation, Inc.
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

"""Interfaces defining email commands."""

from enum import Enum
from public import public
from zope.interface import Attribute, Interface


@public
class ContinueProcessing(Enum):
    """Should `IEmailCommand.process()` continue or not."""
    no = 0
    yes = 1


@public
class IEmailResults(Interface):
    """The email command results object."""

    output = Attribute('An output file object for printing results to.')


@public
class IEmailCommand(Interface):
    """An email command."""

    name = Attribute('Command name as seen in a -request email.')

    argument_description = Attribute('Description of command arguments.')

    description = Attribute('Command help.')

    def process(mlist, msg, msgdata, arguments, results):
        """Process the email command.

        :param mlist: The mailing list target of the command.
        :param msg: The original message object.
        :param msgdata: The message metadata.
        :param arguments: The command arguments tuple.
        :param results: An IEmailResults object for these commands.
        :return: A `ContinueProcessing` enum specifying whether to continue
            processing or not.
        """


@public
class ICLISubCommand(Interface):
    """A command line interface subcommand.

    Subcommands are implemented using the `click` package.  See
    https://click.palletsprojects.com/en/7.x/ for details.
    """
    name = Attribute(
        """The subcommand name as it will show up in `mailman --help`.

        This must be unique; it is a runtime error if any plugin provides a
        subcommand with a clashing name.
        """)

    command = Attribute(
        """The click command to run for this subcommand.

        This must be a function decorated with at least the @click.command()
        decorator.  The function may also be decorated with other arguments as
        needed.
        """)
