# Copyright (C) 2016-2020 by the Free Software Foundation, Inc.
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

"""Test the Join and Leave commands."""

import unittest

from mailman.app.lifecycle import create_list
from mailman.commands.eml_membership import Join, Leave
from mailman.email.message import Message
from mailman.interfaces.bans import IBanManager
from mailman.interfaces.mailinglist import SubscriptionPolicy
from mailman.interfaces.subscriptions import ISubscriptionManager
from mailman.interfaces.usermanager import IUserManager
from mailman.runners.command import Results
from mailman.testing.helpers import set_preferred
from mailman.testing.layers import ConfigLayer
from zope.component import getUtility


class TestLeave(unittest.TestCase):
    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('ant@example.com')
        self._command = Leave()

    def test_confirm_leave_not_a_member(self):
        self._mlist.unsubscription_policy = SubscriptionPolicy.confirm
        # Try to unsubscribe someone who is not a member.  Anne is a real
        # user, with a validated address, but she is not a member of the
        # mailing list.
        anne = getUtility(IUserManager).create_user('anne@example.com')
        set_preferred(anne)
        # Initiate an unsubscription.
        msg = Message()
        msg['From'] = 'anne@example.com'
        results = Results()
        self._command.process(self._mlist, msg, {}, (), results)
        self.assertEqual(
            str(results).splitlines()[-1],
            'leave: anne@example.com is not a member of ant@example.com')


class TestJoin(unittest.TestCase):
    layer = ConfigLayer

    def setUp(self):
        self._mlist = create_list('ant@example.com')
        self._command = Join()

    def test_join_already_a_member(self):
        # Try to subscribe someone who is already a member.  Anne is a real
        # user, with a validated address, but she is not a member of the
        # mailing list yet.
        anne = getUtility(IUserManager).create_user('anne@example.com')
        set_preferred(anne)
        # First subscribe anne.
        ISubscriptionManager(self._mlist).register(anne, pre_verified=True,
                                                   pre_confirmed=True,
                                                   pre_approved=True)
        # Then initiate a subscription.
        msg = Message()
        msg['From'] = 'anne@example.com'
        results = Results()
        self._command.process(self._mlist, msg, {}, (), results)
        self.assertEqual(
            str(results).splitlines()[-1],
            'anne@example.com is already a MemberRole.member of '
            'mailing list ant@example.com')

    def test_join_banned(self):
        # Try to subscribe someone who is banned.  Anne is a real
        # user, with a validated address, but she is not a member of the
        # mailing list and is banned from joining.
        # Add anne to the ban list.
        IBanManager(self._mlist).ban('anne@example.com')
        # Then initiate a subscription.
        msg = Message()
        msg['From'] = 'anne@example.com'
        results = Results()
        self._command.process(self._mlist, msg, {}, (), results)
        self.assertEqual(
            str(results).splitlines()[-1],
            'anne@example.com is not allowed to subscribe to ant@example.com')

    def test_join_pending(self):
        self._mlist.subscription_policy = SubscriptionPolicy.confirm
        # Try to subscribe someone who already has a subscription pending.
        # Anne is a real user, with a validated address, who already has a
        # pending subscription for this mailing list.
        anne = getUtility(IUserManager).create_user('anne@example.com')
        set_preferred(anne)
        # Initiate a subscription.
        ISubscriptionManager(self._mlist).register(anne)
        # And try to subscribe.
        msg = Message()
        msg['From'] = 'anne@example.com'
        results = Results()
        self._command.process(self._mlist, msg, {}, (), results)
        self.assertEqual(
            str(results).splitlines()[-1],
            'anne@example.com has a pending subscription for ant@example.com')

    def test_join_posting_address(self):
        # Try to subscribe the list posting address.
        msg = Message()
        msg['From'] = self._mlist.posting_address
        results = Results()
        self._command.process(self._mlist, msg, {}, (), results)
        self.assertEqual(
            str(results).splitlines()[-1],
            'List posting address not allowed')
