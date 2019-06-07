# Copyright (C) 2009-2019 by the Free Software Foundation, Inc.
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

"""Filesystem utilities."""

import os

from contextlib import suppress
from public import public


@public
class umask:
    """Manage the umask for the with statement."""

    def __init__(self, umask):
        self._umask = umask
        self._old_umask = None

    def __enter__(self):
        assert self._old_umask is None, 'Unexpected existing umask'
        self._old_umask = os.umask(self._umask)

    def __exit__(self, *exc_info):
        assert self._old_umask is not None, 'No previous umask'
        os.umask(self._old_umask)
        # Do not suppress exceptions.
        return False


@public
def makedirs(path, mode=0o0755):
    """Create a directory hierarchy, ensuring permissions.

    Other than just calling os.makedirs(), this ensures that the umask is
    reset so that the makedirs mode will be honored.

    :param path: The directory path to create.
    :type path: string
    :param mode: The numeric permission mode to use.
    :type mode: int
    """
    with umask(0):
        # In order for os.walk to set permissions appropriately if required,
        # the FIRST NON EXISTENT parent directory of the one we wanted to
        # create has to be provided.
        upwards = first_inexistent_directory(path)

        # The directory exists, nothing to do.
        if upwards is None:
            return

        try:
            os.makedirs(path, mode)
        except FileExistsError:
            if not os.path.isdir(path):
                raise FileExistsError((
                   "A race condition might have happened. {} actually "
                   "exists and is not a directory.").format(path))

    # Some systems such as FreeBSD ignore mkdir's mode, so walk the just
    # created directories and try to set the mode, ignoring any OSErrors that
    # occur here.
    for dirpath, dirnames, filenames in os.walk(upwards):
        with suppress(OSError):
            os.chmod(dirpath, mode)


@public
def safe_remove(path):
    with suppress(FileNotFoundError):
        os.remove(path)


def first_inexistent_directory(path):
    """Splits iteratively a path until it gives the first non-existent
    directory in the tree.

    That is, if /home/user/foo/bar/baz is given to the function, and
    /home/user/foo/bar doesn't exist but /home/user/foo exists, returns
    /home/user/foo/bar.
    """
    directory = path
    rhs = None

    while True:
        if os.path.isdir(directory):
            if rhs is None:
                return None
            else:
                return os.path.join(directory, rhs)
        elif os.path.exists(directory):
            raise FileExistsError(
                "The path %s exists but is not a directory.",
                directory)
        directory, rhs = os.path.split(directory)
