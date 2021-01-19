# Copyright (C) 2007-2021 by the Free Software Foundation, Inc.
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

"""Sending notifications."""

import logging

from email.utils import formataddr
from lazr.config import as_boolean
from mailman.config import config
from mailman.core.i18n import _
from mailman.email.message import OwnerNotification, UserNotification
from mailman.interfaces.member import DeliveryMode
from mailman.interfaces.template import ITemplateLoader
from mailman.utilities.string import expand, wrap
from public import public
from zope.component import getUtility


log = logging.getLogger('mailman.error')


@public
def send_welcome_message(mlist, member, language, text=''):
    """Send a welcome message to a subscriber.

    Prepending to the standard welcome message template is the mailing list's
    welcome message, if there is one.

    :param mlist: The mailing list.
    :type mlist: IMailingList
    :param member: The member to send the welcome message to.
    :param address: IMember
    :param language: The language of the response.
    :type language: ILanguage
    """
    welcome_message = wrap(getUtility(ITemplateLoader).get(
        'list:user:notice:welcome', mlist, language=language.code))
    display_name = member.display_name
    # Get the text from the template.
    text = expand(welcome_message, mlist, dict(
        user_name=display_name,
        user_email=member.address.email,
        # For backward compatibility.
        user_address=member.address.email,
        fqdn_listname=mlist.fqdn_listname,
        list_name=mlist.display_name,
        list_requests=mlist.request_address,
        ))
    digmode = (''                                   # noqa: F841
               if member.delivery_mode is DeliveryMode.regular
               else _(' (Digest mode)'))
    msg = UserNotification(
        formataddr((display_name, member.address.email)),
        mlist.request_address,
        _('Welcome to the "$mlist.display_name" mailing list${digmode}'),
        text, language)
    msg['X-No-Archive'] = 'yes'
    msg.send(mlist, verp=as_boolean(config.mta.verp_personalized_deliveries))


@public
def send_goodbye_message(mlist, address, language):
    """Send a goodbye message to a subscriber.

    Prepending to the standard goodbye message template is the mailing list's
    goodbye message, if there is one.

    :param mlist: the mailing list
    :type mlist: IMailingList
    :param address: The address to respond to
    :type address: string
    :param language: the language of the response
    :type language: ILanguage
    """
    goodbye_message = wrap(getUtility(ITemplateLoader).get(
        'list:user:notice:goodbye', mlist, language=language.code))
    msg = UserNotification(
        address, mlist.bounces_address,
        _('You have been unsubscribed from the $mlist.display_name '
          'mailing list'),
        goodbye_message, language)
    msg.send(mlist, verp=as_boolean(config.mta.verp_personalized_deliveries))


@public
def send_admin_subscription_notice(mlist, address, display_name):
    """Send the list administrators a subscription notice.

    :param mlist: The mailing list.
    :type mlist: IMailingList
    :param address: The address being subscribed.
    :type address: string
    :param display_name: The name of the subscriber.
    :type display_name: string
    """
    with _.using(mlist.preferred_language.code):
        subject = _('$mlist.display_name subscription notification')
    text = expand(
        getUtility(ITemplateLoader).get('list:admin:notice:subscribe', mlist),
        mlist, dict(
            member=formataddr((display_name, address)),
            ))
    msg = OwnerNotification(mlist, subject, text, roster=mlist.administrators)
    msg.send(mlist)


@public
def send_admin_disable_notice(mlist, address, display_name):
    """Send the list administrators a membership disabled by-bounce notice.

    :param mlist: The mailing list
    :type mlist: IMailingList
    :param address: The address of the member
    :type address: string
    :param display_name: The name of the subscriber
    :type display_name: string
    """
    member = formataddr((display_name, address))
    data = {'member': member}
    with _.using(mlist.preferred_language.code):
        subject = _('$member\'s subscription disabled on $mlist.display_name')
    text = expand(
        getUtility(ITemplateLoader).get('list:admin:notice:disable', mlist),
        mlist, data)
    msg = OwnerNotification(mlist, subject, text, roster=mlist.administrators)
    msg.send(mlist)


def send_admin_removal_notice(mlist, address, display_name):
    """Send the list administrators a membership removed due to bounce notice.

    :param mlist: The mailing list.
    :type mlist: IMailingList
    :param address: The address of the member
    :type address: string
    :param display_name: The name of the subscriber
    :type display_name: string
    """
    member = formataddr((display_name, address))
    data = {'member': member, 'mlist': mlist.display_name}
    with _.using(mlist.preferred_language.code):
        subject = _('$member unsubscribed from ${mlist.display_name} '
                    'mailing list due to bounces')
    text = expand(
        getUtility(ITemplateLoader).get('list:admin:notice:removal', mlist),
        mlist, data)
    msg = OwnerNotification(mlist, subject, text, roster=mlist.administrators)
    msg.send(mlist)


@public
def send_user_disable_warning(mlist, address, language):
    """Sends a warning mail to the user reminding the person to
    reenable its DeliveryStatus.

    :param mlist: The mailing list
    :type mlist: IMailingList
    :param address: The address of the member
    :type address: string.
    :param language: member's preferred language
    :type language: ILanguage
    """
    warning_message = wrap(getUtility(ITemplateLoader).get(
        'list:user:notice:warning', mlist, language=language.code))
    warning_message_text = expand(
        warning_message, mlist, dict(sender_email=address))
    msg = UserNotification(
        address, mlist.bounces_address,
        _('Your subscription for ${mlist.display_name} mailing list'
          ' has been disabled'),
        warning_message_text, language)
    msg.send(mlist, verp=as_boolean(config.mta.verp_personalized_deliveries))
