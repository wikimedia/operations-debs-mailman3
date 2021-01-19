# Copyright (C) 2014-2021 by the Free Software Foundation, Inc.
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

"""Test the Subject header prefix munging.."""

import unittest

from mailman.app.lifecycle import create_list
from mailman.config import config
from mailman.email.message import Message
from mailman.interfaces.languages import ILanguageManager
from mailman.testing.layers import ConfigLayer
from zope.component import getUtility


class TestSubjectPrefix(unittest.TestCase):
    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('test@example.com')
        self._process = config.handlers['subject-prefix'].process

    def test_isdigest(self):
        # If the message is destined for the digest, the Subject header does
        # not get touched.
        msg = Message()
        msg['Subject'] = 'A test message'
        self._process(self._mlist, msg, dict(isdigest=True))
        self.assertEqual(str(msg['subject']), 'A test message')

    def test_fasttrack(self):
        # Messages internally crafted are 'fast tracked' and don't get their
        # Subjects prefixed either.
        msg = Message()
        msg['Subject'] = 'A test message'
        self._process(self._mlist, msg, dict(_fasttrack=True))
        self.assertEqual(str(msg['subject']), 'A test message')

    def test_whitespace_only_prefix(self):
        # If the Subject prefix only contains whitespace, ignore it.
        self._mlist.subject_prefix = '    '
        msg = Message()
        msg['Subject'] = 'A test message'
        self._process(self._mlist, msg, {})
        self.assertEqual(str(msg['subject']), 'A test message')

    def test_save_original_subject(self):
        # When the Subject gets prefixed, the original is saved in the message
        # metadata.
        msgdata = {}
        msg = Message()
        msg['Subject'] = 'A test message'
        self._process(self._mlist, msg, msgdata)
        self.assertEqual(msgdata['original_subject'], 'A test message')

    def test_prefix(self):
        # The Subject gets prefixed.  The prefix gets automatically set by the
        # list style when the list gets created.
        msg = Message()
        msg['Subject'] = 'A test message'
        self._process(self._mlist, msg, {})
        self.assertEqual(str(msg['subject']), '[Test] A test message')

    def test_no_double_prefix(self):
        # Don't add a prefix if the subject already contains one.
        msg = Message()
        msg['Subject'] = '[Test] A test message'
        self._process(self._mlist, msg, {})
        self.assertEqual(str(msg['subject']), '[Test] A test message')

    def test_re_prefix(self):
        # The subject has a Re: prefix.  Make sure that gets preserved, but
        # after the list prefix.
        msg = Message()
        msg['Subject'] = 'Re: [Test] A test message'
        self._process(self._mlist, msg, {})
        self.assertEqual(str(msg['subject']), '[Test] Re: A test message')

    def test_re_prefix_all_same(self):
        # Re: prefix with non-ascii.
        msg = Message()
        msg['Subject'] = '=?utf-8?Q?Re:_[Test]_A_test_message?='
        old_charset = self._mlist.preferred_language.charset
        self._mlist.preferred_language.charset = 'utf-8'
        self._process(self._mlist, msg, {})
        self._mlist.preferred_language.charset = old_charset
        self.assertEqual(str(msg['subject']), '[Test] Re: A test message')

    def test_re_prefix_mixed(self):
        # Re: prefix with non-ascii and mixed charset.
        msg = Message()
        msg['Subject'] = '=?utf-8?Q?Re:_[Test]_A_test_message?='
        self._process(self._mlist, msg, {})
        self.assertEqual(str(msg['subject']), '[Test] Re: A test message')

    def test_multiline_subject(self):
        # The subject appears on multiple lines.
        msg = Message()
        msg['Subject'] = '\n A test message'
        self._process(self._mlist, msg, {})
        self.assertEqual(str(msg['subject']), '[Test]  A test message')

    def test_i18n_prefix(self):
        # The Subject header is encoded, but the prefix is still added.
        msg = Message()
        msg['Subject'] = '=?iso-2022-jp?b?GyRCJWEhPCVrJV4lcxsoQg==?='
        self._process(self._mlist, msg, {})
        subject = msg['subject']
        self.assertEqual(subject.encode(),
                         '[Test] =?iso-2022-jp?b?GyRCJWEhPCVrJV4lcxsoQg==?=')
        self.assertEqual(str(subject), '[Test] メールマン')

    def test_prefix_only(self):
        # Incoming subject is only the prefix.
        msg = Message()
        msg['Subject'] = '[Test] '
        self._process(self._mlist, msg, {})
        subject = msg['subject']
        self.assertEqual(str(subject), '[Test] ')

    def test_prefix_only_all_same(self):
        # Incoming subject is only the prefix.
        msg = Message()
        msg['Subject'] = '=?utf-8?Q?[Test]_?='
        old_charset = self._mlist.preferred_language.charset
        self._mlist.preferred_language.charset = 'utf-8'
        self._process(self._mlist, msg, {})
        self._mlist.preferred_language.charset = old_charset
        subject = msg['subject']
        self.assertEqual(str(subject), '[Test] ')

    def test_prefix_only_mixed(self):
        # Incoming subject is only the prefix.
        msg = Message()
        msg['Subject'] = '=?utf-8?Q?[Test]_?='
        self._process(self._mlist, msg, {})
        subject = msg['subject']
        self.assertEqual(str(subject), '[Test] ')

    def test_re_only(self):
        # Incoming subject is only Re:.
        msg = Message()
        msg['Subject'] = 'Re:'
        self._process(self._mlist, msg, {})
        subject = msg['subject']
        self.assertEqual(str(subject), '[Test] Re: ')

    def test_re_only_all_same(self):
        # Incoming subject is only Re:.
        msg = Message()
        msg['Subject'] = '=?utf-8?Q?Re:?='
        old_charset = self._mlist.preferred_language.charset
        self._mlist.preferred_language.charset = 'utf-8'
        self._process(self._mlist, msg, {})
        self._mlist.preferred_language.charset = old_charset
        subject = msg['subject']
        self.assertEqual(str(subject), '[Test] Re: ')

    def test_re_only_mixed(self):
        # Incoming subject is only Re:.
        msg = Message()
        msg['Subject'] = '=?utf-8?Q?Re:?='
        self._process(self._mlist, msg, {})
        subject = msg['subject']
        self.assertEqual(str(subject), '[Test] Re: ')

    def test_i18n_subject_with_sequential_prefix_and_re(self):
        # The mailing list defines a sequential prefix, and the original
        # Subject has a prefix with a different sequence number, *and* it also
        # contains a Re: prefix.  Make sure the sequence gets updated and all
        # the bits get put back together in the right order.
        self._mlist.subject_prefix = '[Test %d]'
        self._mlist.post_id = 456
        msg = Message()
        msg['Subject'] = \
            '[Test 123] Re: =?iso-2022-jp?b?GyRCJWEhPCVrJV4lcxsoQg==?='
        self._process(self._mlist, msg, {})
        subject = msg['subject']
        self.assertEqual(
            subject.encode(),
            '[Test 456] Re: =?iso-2022-jp?b?GyRCJWEhPCVrJV4lcxsoQg==?=')
        self.assertEqual(str(subject), '[Test 456] Re: メールマン')

    def test_decode_header_returns_string(self):
        # Under some circumstances, email.header.decode_header() returns a
        # string value.  Ensure we can handle that.
        manager = getUtility(ILanguageManager)
        manager.add('xx', 'iso-8859-1', 'Xlandia')
        self._mlist.preferred_language = 'xx'
        msg = Message()
        msg['Subject'] = 'Plain text'
        self._process(self._mlist, msg, {})
        subject = msg['subject']
        self.assertEqual(subject.encode(),
                         '=?iso-8859-1?q?=5BTest=5D_?= Plain text')

    def test_unknown_encoded_subject(self):
        msg = Message()
        msg['Subject'] = '=?unknown-8bit?q?Non-ascii_subject_-_français?='
        self._process(self._mlist, msg, {})
        subject = msg['subject']
        self.assertEqual(str(subject),
                         '[Test]  Non-ascii subject - fran�ais')
