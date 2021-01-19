# Copyright (C) 2012-2021 by the Free Software Foundation, Inc.
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

"""Test the mime_delete handler."""

import os
import sys
import email
import shutil
import tempfile
import unittest

from contextlib import ExitStack, contextmanager
from importlib_resources import open_binary as resource_open, read_text
from io import StringIO
from mailman.app.lifecycle import create_list
from mailman.config import config
from mailman.handlers import mime_delete
from mailman.interfaces.action import FilterAction
from mailman.interfaces.member import MemberRole
from mailman.interfaces.pipeline import DiscardMessage, RejectMessage
from mailman.interfaces.usermanager import IUserManager
from mailman.testing.helpers import (
    LogFileMark, configuration, get_queue_messages,
    specialized_message_from_string as mfs)
from mailman.testing.layers import ConfigLayer
from unittest.mock import patch
from zope.component import getUtility


@contextmanager
def dummy_script(arg=''):
    exe = sys.executable
    non_ascii = ''
    if arg == 'non-ascii':
        non_ascii = '‘...’'
    extra = ''
    if arg == 'scripterr':
        extra = 'error'
    with ExitStack() as resources:
        tempdir = tempfile.mkdtemp()
        resources.callback(shutil.rmtree, tempdir)
        filter_path = os.path.join(tempdir, 'filter.py')
        if arg in ('noperm', 'nonexist'):
            exe = filter_path
        with open(filter_path, 'w', encoding='utf-8') as fp:
            print("""\
import sys
if len(sys.argv) > 2:
    sys.exit(1)
print('Converted text/html to text/plain{}')
print('Filename:', sys.argv[1])
print(open(sys.argv[1]).readlines()[0])
""".format(non_ascii), file=fp)
        config.push('dummy script', """\
[mailman]
html_to_plain_text_command = {exe} {script} {extra} $filename
""".format(exe=exe, script=filter_path, extra=extra))
        resources.callback(config.pop, 'dummy script')
        if arg == 'nonexist':
            os.rename(filter_path, filter_path + 'xxx')
        elif arg == 'noperm':
            os.chmod(filter_path, 0o644)
        yield


class TestDispose(unittest.TestCase):
    """Test the mime_delete handler."""

    layer = ConfigLayer
    maxxDiff = None

    def setUp(self):
        self._mlist = create_list('test@example.com')
        self._msg = mfs("""\
From: anne@example.com
To: test@example.com
Subject: A disposable message
Message-ID: <ant>

""")
        config.push('dispose', """
        [mailman]
        site_owner: noreply@example.com
        """)
        self.addCleanup(config.pop, 'dispose')

    def test_dispose_discard(self):
        self._mlist.filter_action = FilterAction.discard
        with self.assertRaises(DiscardMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'discarding')
        self.assertEqual(cm.exception.message, 'discarding')
        # There should be no messages in the 'bad' queue.
        get_queue_messages('bad', expected_count=0)

    def test_dispose_discard_no_spurious_log(self):
        self._mlist.filter_action = FilterAction.discard
        mark = LogFileMark('mailman.error')
        with self.assertRaises(DiscardMessage):
            mime_delete.dispose(self._mlist, self._msg, {}, 'discarding')
        self.assertEqual(mark.readline(), '')

    def test_dispose_bounce(self):
        self._mlist.filter_action = FilterAction.reject
        with self.assertRaises(RejectMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'rejecting')
        self.assertEqual(cm.exception.message, 'rejecting')
        # There should be no messages in the 'bad' queue.
        get_queue_messages('bad', expected_count=0)

    def test_dispose_forward(self):
        # The disposed message gets forwarded to the list administrators.  So
        # first add an owner and a moderator.
        user_manager = getUtility(IUserManager)
        anne = user_manager.create_address('anne@example.com')
        bart = user_manager.create_address('bart@example.com')
        self._mlist.subscribe(anne, MemberRole.owner)
        self._mlist.subscribe(bart, MemberRole.moderator)
        # Now set the filter action and dispose the message.
        self._mlist.filter_action = FilterAction.forward
        with self.assertRaises(DiscardMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'forwarding')
        self.assertEqual(cm.exception.message, 'forwarding')
        # There should now be a multipart message in the virgin queue destined
        # for the mailing list owners.
        items = get_queue_messages('virgin', expected_count=1)
        message = items[0].msg
        self.assertEqual(message.get_content_type(), 'multipart/mixed')
        # Anne and Bart should be recipients of the message, but it will look
        # like the message is going to the list owners.
        self.assertEqual(message['to'], 'test-owner@example.com')
        self.assertEqual(message.recipients,
                         set(['anne@example.com', 'bart@example.com']))
        # The list owner should be the sender.
        self.assertEqual(message['from'], 'noreply@example.com')
        self.assertEqual(message['subject'],
                         'Content filter message notification')
        # The body of the first part provides the moderators some details.
        part0 = message.get_payload(0)
        self.assertEqual(part0.get_content_type(), 'text/plain')
        self.assertMultiLineEqual(part0.get_payload(), """\
The attached message matched the Test mailing list's content
filtering rules and was prevented from being forwarded on to the list
membership.  You are receiving the only remaining copy of the discarded
message.

""")
        # The second part is the container for the original message.
        part1 = message.get_payload(1)
        self.assertEqual(part1.get_content_type(), 'message/rfc822')
        # And the first part of *that* message will be the original message.
        original = part1.get_payload(0)
        self.assertEqual(original['subject'], 'A disposable message')
        self.assertEqual(original['message-id'], '<ant>')

    @configuration('mailman', filtered_messages_are_preservable='no')
    def test_dispose_non_preservable(self):
        # Two actions can happen here, depending on a site-wide setting.  If
        # the site owner has indicated that filtered messages cannot be
        # preserved, then this is the same as discarding them.
        self._mlist.filter_action = FilterAction.preserve
        with self.assertRaises(DiscardMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'not preserved')
        self.assertEqual(cm.exception.message, 'not preserved')
        # There should be no messages in the 'bad' queue.
        get_queue_messages('bad', expected_count=0)

    @configuration('mailman', filtered_messages_are_preservable='yes')
    def test_dispose_preservable(self):
        # Two actions can happen here, depending on a site-wide setting.  If
        # the site owner has indicated that filtered messages can be
        # preserved, then this is similar to discarding the message except
        # that a copy is preserved in the 'bad' queue.
        self._mlist.filter_action = FilterAction.preserve
        with self.assertRaises(DiscardMessage) as cm:
            mime_delete.dispose(self._mlist, self._msg, {}, 'preserved')
        self.assertEqual(cm.exception.message, 'preserved')
        # There should be no messages in the 'bad' queue.
        items = get_queue_messages('bad', expected_count=1)
        message = items[0].msg
        self.assertEqual(message['subject'], 'A disposable message')
        self.assertEqual(message['message-id'], '<ant>')

    def test_bad_action(self):
        # This should never happen, but what if it does?
        # FilterAction.accept, FilterAction.hold, and FilterAction.defer are
        # not valid.  They are treated as discard actions, but the problem is
        # also logged.
        for action in (FilterAction.accept,
                       FilterAction.hold,
                       FilterAction.defer):
            self._mlist.filter_action = action
            mark = LogFileMark('mailman.error')
            with self.assertRaises(DiscardMessage) as cm:
                mime_delete.dispose(self._mlist, self._msg, {}, 'bad action')
            self.assertEqual(cm.exception.message, 'bad action')
            line = mark.readline()[:-1]
            self.assertTrue(line.endswith(
                'test@example.com invalid FilterAction: {}.  '
                'Treating as discard'.format(action.name)))


class TestHTMLFilter(unittest.TestCase):
    """Test the conversion of HTML to plaintext."""

    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')
        self._mlist.convert_html_to_plaintext = True
        self._mlist.filter_content = True

    def test_convert_html_to_plaintext(self):
        # Converting to plain text calls a command line script.
        msg = mfs("""\
From: aperson@example.com
Content-Type: text/html
MIME-Version: 1.0

<html><head></head>
<body></body></html>
""")
        process = config.handlers['mime-delete'].process
        with dummy_script():
            process(self._mlist, msg, {})
        self.assertEqual(msg.get_content_type(), 'text/plain')
        self.assertTrue(
            msg['x-content-filtered-by'].startswith('Mailman/MimeDel'))
        payload_lines = msg.get_payload().splitlines()
        self.assertEqual(payload_lines[0], 'Converted text/html to text/plain')

    def test_convert_html_to_plaintext_base64(self):
        # Converting to plain text calls a command line script with decoded
        # message body.
        msg = mfs("""\
From: aperson@example.com
Content-Type: text/html
Content-Transfer-Encoding: base64
MIME-Version: 1.0

PGh0bWw+PGhlYWQ+PC9oZWFkPgo8Ym9keT48L2JvZHk+PC9odG1sPgo=
""")
        process = config.handlers['mime-delete'].process
        with dummy_script():
            process(self._mlist, msg, {})
        self.assertEqual(msg.get_content_type(), 'text/plain')
        self.assertTrue(
            msg['x-content-filtered-by'].startswith('Mailman/MimeDel'))
        payload_lines = msg.get_payload().splitlines()
        self.assertEqual(payload_lines[0], 'Converted text/html to text/plain')
        self.assertEqual(payload_lines[2], '<html><head></head>')

    def test_convert_html_to_plaintext_encodes_new_payload(self):
        # Test that the converted payload with non-ascii is encoded.
        msg = mfs("""\
From: aperson@example.com
Content-Type: text/html; charset=utf-8
Content-Transfer-Encoding: base64
MIME-Version: 1.0

Q29udmVydGVkIHRleHQvaHRtbCB0byB0ZXh0L3BsYWlu4oCYLi4u4oCZCg==
""")
        process = config.handlers['mime-delete'].process
        with dummy_script('non-ascii'):
            process(self._mlist, msg, {})
        self.assertEqual(msg['content-type'], 'text/plain; charset="utf-8"')
        self.assertEqual(msg['content-transfer-encoding'], 'base64')
        self.assertTrue(
            msg['x-content-filtered-by'].startswith('Mailman/MimeDel'))
        payload_lines = (
            msg.get_payload(decode=True).decode('utf-8').splitlines())
        self.assertEqual(payload_lines[0],
                         'Converted text/html to text/plain‘...’')
        self.assertTrue(payload_lines[1].startswith('Filename'))

    def test_convert_html_to_plaintext_error_return(self):
        # Calling a script which returns an error status is properly logged.
        msg = mfs("""\
From: aperson@example.com
Content-Type: text/html
MIME-Version: 1.0

<html><head></head>
<body></body></html>
""")
        process = config.handlers['mime-delete'].process
        mark = LogFileMark('mailman.error')
        with dummy_script('scripterr'):
            process(self._mlist, msg, {})
        line = mark.readline()[:-1]
        self.assertTrue(line.endswith('HTML -> text/plain command error'))
        self.assertEqual(msg.get_content_type(), 'text/html')
        self.assertIsNone(msg['x-content-filtered-by'])
        payload_lines = msg.get_payload().splitlines()
        self.assertEqual(payload_lines[0], '<html><head></head>')

    def test_missing_html_to_plain_text_command(self):
        # Calling a missing html_to_plain_text_command is properly logged.
        msg = mfs("""\
From: aperson@example.com
Content-Type: text/html
MIME-Version: 1.0

<html><head></head>
<body></body></html>
""")
        process = config.handlers['mime-delete'].process
        mark = LogFileMark('mailman.error')
        with dummy_script('nonexist'):
            process(self._mlist, msg, {})
        line = mark.readline()[:-1]
        self.assertTrue(line.endswith('HTML -> text/plain command error'))
        self.assertEqual(msg.get_content_type(), 'text/html')
        self.assertIsNone(msg['x-content-filtered-by'])
        payload_lines = msg.get_payload().splitlines()
        self.assertEqual(payload_lines[0], '<html><head></head>')

    def test_no_permission_html_to_plain_text_command(self):
        # Calling an html_to_plain_text_command without permission is
        # properly logged.
        msg = mfs("""\
From: aperson@example.com
Content-Type: text/html
MIME-Version: 1.0

<html><head></head>
<body></body></html>
""")
        process = config.handlers['mime-delete'].process
        mark = LogFileMark('mailman.error')
        with dummy_script('noperm'):
            process(self._mlist, msg, {})
        line = mark.readline()[:-1]
        self.assertTrue(line.endswith('HTML -> text/plain command error'))
        self.assertEqual(msg.get_content_type(), 'text/html')
        self.assertIsNone(msg['x-content-filtered-by'])
        payload_lines = msg.get_payload().splitlines()
        self.assertEqual(payload_lines[0], '<html><head></head>')

    def test_html_part_with_non_ascii(self):
        # Ensure we can convert HTML to plain text in an HTML sub-part which
        # contains non-ascii.
        with resource_open(
                'mailman.handlers.tests.data',
                'html_to_plain.eml') as fp:
            msg = email.message_from_binary_file(fp)
        process = config.handlers['mime-delete'].process
        with dummy_script():
            process(self._mlist, msg, {})
        part = msg.get_payload(1)
        cset = part.get_content_charset('us-ascii')
        text = part.get_payload(decode=True).decode(cset).splitlines()
        self.assertEqual(text[0], 'Converted text/html to text/plain')
        self.assertEqual(text[2], 'Um frühere Nachrichten')


class TestMiscellaneous(unittest.TestCase):
    """Test various miscellaneous filtering actions."""

    layer = ConfigLayer
    maxDiff = None

    def setUp(self):
        self._mlist = create_list('test@example.com')
        self._mlist.collapse_alternatives = True
        self._mlist.filter_content = True
        self._mlist.filter_extensions = ['xlsx']

    def test_collapse_alternatives(self):
        with resource_open(
                'mailman.handlers.tests.data',
                'collapse_alternatives.eml') as fp:
            msg = email.message_from_binary_file(fp)
        process = config.handlers['mime-delete'].process
        process(self._mlist, msg, {})
        structure = StringIO()
        email.iterators._structure(msg, fp=structure)
        self.assertEqual(structure.getvalue(), """\
multipart/signed
    multipart/mixed
        text/plain
        text/plain
    application/pgp-signature
""")

    def test_collapse_alternatives_non_ascii(self):
        # Ensure we can flatten as bytes a message whose non-ascii payload
        # has been reset.
        with resource_open(
                'mailman.handlers.tests.data',
                'c_a_non_ascii.eml') as fp:
            msg = email.message_from_binary_file(fp)
        process = config.handlers['mime-delete'].process
        process(self._mlist, msg, {})
        self.assertFalse(msg.is_multipart())
        self.assertEqual(msg.get_payload(decode=True),
                         b'Body with non-ascii can\xe2\x80\x99t see '
                         b'won\xe2\x80\x99t know\n')
        # Ensure we can flatten it.
        dummy = msg.as_bytes()                             # noqa: F841

    def test_collapse_alternatives_non_ascii_encoded(self):
        msg = mfs("""\
From: anne@example.com
To: test@example.com
Subject: Testing mpa with transfer encoded subparts
Message-ID: <ant>
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="AAAA"

--AAAA
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable

Let=E2=80=99s also consider

--AAAA
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: quoted-printable

Let=E2=80=99s also consider

--AAAA--
""")
        process = config.handlers['mime-delete'].process
        process(self._mlist, msg, {})
        self.assertFalse(msg.is_multipart())
        self.assertEqual(msg.get_payload(decode=True),
                         b'Let\xe2\x80\x99s also consider\n')
        # Ensure we can flatten it.
        dummy = msg.as_bytes()                             # noqa: F841

    def test_reset_payload_multipart(self):
        msg = mfs("""\
From: anne@example.com
To: test@example.com
Subject: Testing mpa with multipart subparts
Message-ID: <ant>
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="AAAA"

--AAAA
Content-Type: multipart/mixed; boundary="BBBB"

--BBBB
Content-Type: text/plain

Part 1

--BBBB
Content-Type: text/plain

Part 2

--BBBB--

--AAAA
Content-Type: multipart/mixed; boundary="CCCC"

--CCCC
Content-Type: text/html

Part 3

--CCCC
Content-Type: text/html

Part 4

--CCCC--

--AAAA--
""")
        process = config.handlers['mime-delete'].process
        process(self._mlist, msg, {})
        self.assertTrue(msg.is_multipart())
        self.assertEqual(msg.get_content_type(), 'multipart/mixed')
        self.assertEqual(len(msg.get_payload()), 2)
        self.assertEqual(msg.get_payload(0).get_payload(), 'Part 1\n')
        self.assertEqual(msg.get_payload(1).get_payload(), 'Part 2\n')

    def test_msg_rfc822(self):
        with resource_open(
                'mailman.handlers.tests.data', 'msg_rfc822.eml') as fp:
            msg = email.message_from_binary_file(fp)
        process = config.handlers['mime-delete'].process
        # Mock this so that the X-Content-Filtered-By header isn't sensitive to
        # Mailman version bumps.
        with patch('mailman.handlers.mime_delete.VERSION', '123'):
            expected_msg = read_text(
                'mailman.handlers.tests.data', 'msg_rfc822_out.eml')
            process(self._mlist, msg, {})
            self.assertEqual(msg.as_string(), expected_msg)

    def test_mixed_case_ext_and_recast(self):
        msg = mfs("""\
From: anne@example.com
To: test@example.com
Subject: Testing mixed extension
Message-ID: <ant>
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="AAAA"

--AAAA
Content-Type: text/plain; charset="utf-8"

Plain text

--AAAA
Content-Type: application/octet-stream; name="test.xlsX"
Content-Disposition: attachment; filename="test.xlsX"

spreadsheet

--AAAA--
""")
        process = config.handlers['mime-delete'].process
        process(self._mlist, msg, {})
        self.assertEqual(msg['content-type'], 'text/plain; charset="utf-8"')
        self.assertEqual(msg.get_payload(decode=True), b"""\
Plain text
""")
