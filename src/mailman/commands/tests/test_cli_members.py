# Copyright (C) 2015-2021 by the Free Software Foundation, Inc.
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

"""Test the `mailman members` command."""

import unittest

from click.testing import CliRunner
from mailman.app.lifecycle import create_list
from mailman.commands.cli_members import members
from mailman.interfaces.member import MemberRole
from mailman.testing.helpers import subscribe
from mailman.testing.layers import ConfigLayer
from tempfile import NamedTemporaryFile


class TestCLIMembers(unittest.TestCase):
    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('ant@example.com')
        self._command = CliRunner()

    def test_no_such_list(self):
        result = self._command.invoke(members, ('bee.example.com',))
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(
            result.output,
            'Usage: members [OPTIONS] LISTSPEC\n'
            'Try \'members --help\' for help.\n\n'
            'Error: No such list: bee.example.com\n')

    def test_role_administrator(self):
        subscribe(self._mlist, 'Anne', role=MemberRole.owner)
        subscribe(self._mlist, 'Bart', role=MemberRole.moderator)
        subscribe(self._mlist, 'Cate', role=MemberRole.nonmember)
        subscribe(self._mlist, 'Dave', role=MemberRole.member)
        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '--role', 'administrator', '-o', outfp.name,
                'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], 'Anne Person <aperson@example.com>\n')
        self.assertEqual(lines[1], 'Bart Person <bperson@example.com>\n')

    def test_role_any(self):
        subscribe(self._mlist, 'Anne', role=MemberRole.owner)
        subscribe(self._mlist, 'Bart', role=MemberRole.moderator)
        subscribe(self._mlist, 'Cate', role=MemberRole.nonmember)
        subscribe(self._mlist, 'Dave', role=MemberRole.member)
        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '--role', 'any', '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0], 'Anne Person <aperson@example.com>\n')
        self.assertEqual(lines[1], 'Bart Person <bperson@example.com>\n')
        self.assertEqual(lines[2], 'Cate Person <cperson@example.com>\n')
        self.assertEqual(lines[3], 'Dave Person <dperson@example.com>\n')

    def test_role_moderator(self):
        subscribe(self._mlist, 'Anne', role=MemberRole.owner)
        subscribe(self._mlist, 'Bart', role=MemberRole.moderator)
        subscribe(self._mlist, 'Cate', role=MemberRole.nonmember)
        subscribe(self._mlist, 'Dave', role=MemberRole.member)
        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '--role', 'moderator', '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'Bart Person <bperson@example.com>\n')

    def test_role_nonmember(self):
        subscribe(self._mlist, 'Anne', role=MemberRole.owner)
        subscribe(self._mlist, 'Bart', role=MemberRole.moderator)
        subscribe(self._mlist, 'Cate', role=MemberRole.nonmember)
        subscribe(self._mlist, 'Dave', role=MemberRole.member)
        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '--role', 'nonmember', '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'Cate Person <cperson@example.com>\n')

    def test_already_subscribed_with_display_name(self):
        subscribe(self._mlist, 'Anne')
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--add', infp.name, 'ant.example.com'))
        self.assertEqual(
           result.output,
           'Warning: The --add option is deprecated. Use '
           '`mailman addmembers` instead.\n'
           'Already subscribed (skipping): Anne Person <aperson@example.com>\n'
           )

    def test_add_invalid_email(self):
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('foobar@', file=infp)
            result = self._command.invoke(members, (
                '--add', infp.name, 'ant.example.com'))
        self.assertEqual(
           result.output,
           'Warning: The --add option is deprecated. Use '
           '`mailman addmembers` instead.\n'
           'Cannot parse as valid email address (skipping): foobar@\n'
           )

    def test_not_subscribed_without_display_name(self):
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('aperson@example.com', file=infp)
            result = self._command.invoke(members, (
                '--delete', infp.name, 'ant.example.com'))
        self.assertEqual(
           result.output,
           'Warning: The --delete option is deprecated. Use '
           '`mailman delmembers` instead.\n'
           'Member not subscribed (skipping): '
           'aperson@example.com\n'
           )

    def test_not_subscribed_with_display_name(self):
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--delete', infp.name, 'ant.example.com'))
        self.assertEqual(
           result.output,
           'Warning: The --delete option is deprecated. Use '
           '`mailman delmembers` instead.\n'
           'Member not subscribed (skipping): '
           'Anne Person <aperson@example.com>\n'
           )

    def test_deletion_blank_lines(self):
        subscribe(self._mlist, 'Anne')
        subscribe(self._mlist, 'Bart')
        subscribe(self._mlist, 'Cate')
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            print('', file=infp)
            print('   ', file=infp)
            print('\t', file=infp)
            print('Bart Person <bperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--delete', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --delete option is deprecated. Use '
            '`mailman delmembers` instead.\n')
        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'Cate Person <cperson@example.com>\n')

    def test_deletion_commented_lines(self):
        subscribe(self._mlist, 'Anne')
        subscribe(self._mlist, 'Bart')
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            print('#Bart Person <bperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--delete', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --delete option is deprecated. Use '
            '`mailman delmembers` instead.\n')

        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'Bart Person <bperson@example.com>\n')

    def test_sync_invalid_email(self):
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Dont Subscribe <not-a-valid-email>', file=infp)
            print('not-a-valid@email', file=infp)
            result = self._command.invoke(members, (
                '--sync', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --sync option is deprecated. '
            'Use `mailman syncmembers` instead.\n'
            'Cannot parse as valid email address'
            ' (skipping): Dont Subscribe <not-a-valid-email>\n'
            'Cannot parse as valid email address'
            ' (skipping): not-a-valid@email\n'
            'Nothing to do\n')

    def test_sync_no_change(self):
        subscribe(self._mlist, 'Anne')
        subscribe(self._mlist, 'Bart')
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--no-change', '--sync', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --sync option is deprecated. '
            'Use `mailman syncmembers` instead.\n'
            '[DEL] Bart Person <bperson@example.com>\n')

    def test_sync_empty_tuple(self):
        subscribe(self._mlist, 'Anne')
        subscribe(self._mlist, 'Bart')
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            print('\"\"', file=infp)
            result = self._command.invoke(members, (
                '--no-change', '--sync', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --sync option is deprecated. '
            'Use `mailman syncmembers` instead.\n'
            'Cannot parse as valid email address (skipping): ""\n'
            '[DEL] Bart Person <bperson@example.com>\n')

    def test_sync_commented_lines(self):
        subscribe(self._mlist, 'Anne')
        subscribe(self._mlist, 'Bart')
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            print('#Bart Person <bperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--sync', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --sync option is deprecated. '
            'Use `mailman syncmembers` instead.\n'
            '[DEL] Bart Person <bperson@example.com>\n')

        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'Anne Person <aperson@example.com>\n')

    def test_sync_blank_lines(self):
        subscribe(self._mlist, 'Anne')
        subscribe(self._mlist, 'Bart')
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            print('', file=infp)
            print('', file=infp)
            result = self._command.invoke(members, (
                '--sync', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --sync option is deprecated. '
            'Use `mailman syncmembers` instead.\n'
            '[DEL] Bart Person <bperson@example.com>\n')

        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'Anne Person <aperson@example.com>\n')

    def test_sync_nothing_to_do(self):
        subscribe(self._mlist, 'Anne')
        subscribe(self._mlist, 'Bart')
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('Anne Person <aperson@example.com>', file=infp)
            print('Bart Person <bperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--sync', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --sync option is deprecated. '
            'Use `mailman syncmembers` instead.\n'
            'Nothing to do\n')

        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], 'Anne Person <aperson@example.com>\n')
        self.assertEqual(lines[1], 'Bart Person <bperson@example.com>\n')

    def test_sync_no_display_name(self):
        subscribe(self._mlist, 'Bart')
        subscribe(self._mlist, 'Cate', role=MemberRole.nonmember)
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('<aperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--sync', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --sync option is deprecated. '
            'Use `mailman syncmembers` instead.\n'
            '[ADD] aperson@example.com\n'
            '[DEL] Bart Person <bperson@example.com>\n')

        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'aperson@example.com\n')

    def test_sync_del_no_display_name(self):
        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('bperson@example.com', file=infp)
            result = self._command.invoke(members, (
                '--add', infp.name, 'ant.example.com'))

        with NamedTemporaryFile('w', buffering=1, encoding='utf-8') as infp:
            print('<aperson@example.com>', file=infp)
            result = self._command.invoke(members, (
                '--sync', infp.name, 'ant.example.com'))
        self.assertEqual(
            result.output,
            'Warning: The --sync option is deprecated. '
            'Use `mailman syncmembers` instead.\n'
            '[ADD] aperson@example.com\n'
            '[DEL] bperson@example.com\n')

        with NamedTemporaryFile('w', encoding='utf-8') as outfp:
            self._command.invoke(members, (
                '-o', outfp.name, 'ant.example.com'))
            with open(outfp.name, 'r', encoding='utf-8') as infp:
                lines = infp.readlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], 'aperson@example.com\n')

    def test_email_only(self):
        subscribe(self._mlist, 'Anne')
        subscribe(self._mlist, 'Bart')
        result = self._command.invoke(members, (
            '--email-only', 'ant.example.com'))
        self.assertEqual(
            result.output, 'aperson@example.com\nbperson@example.com\n')
