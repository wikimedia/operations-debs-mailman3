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

"""The 'members' subcommand."""

import sys
import click

from email.utils import formataddr, parseaddr
from mailman.app.membership import add_member, delete_member
from mailman.core.i18n import _
from mailman.database.transaction import transactional
from mailman.interfaces.address import InvalidEmailAddressError
from mailman.interfaces.command import ICLISubCommand
from mailman.interfaces.listmanager import IListManager
from mailman.interfaces.member import (
    AlreadySubscribedError, DeliveryMode, DeliveryStatus,
    MemberRole, NotAMemberError)
from mailman.interfaces.subscriptions import RequestRecord
from mailman.utilities.options import I18nCommand
from operator import attrgetter
from public import public
from zope.component import getUtility
from zope.interface import implementer


def display_members(ctx, mlist, role, regular, digest, nomail, outfp):
    # Which type of digest recipients should we display?
    if digest == 'any':
        digest_types = [
            DeliveryMode.plaintext_digests,
            DeliveryMode.mime_digests,
            DeliveryMode.summary_digests,
            ]
    elif digest is not None:
        digest_types = [DeliveryMode[digest + '_digests']]
    else:
        # Don't filter on digest type.
        pass
    # Which members with delivery disabled should we display?
    if nomail is None:
        # Don't filter on delivery status.
        pass
    elif nomail == 'byadmin':
        status_types = [DeliveryStatus.by_moderator]
    elif nomail.startswith('by'):
        status_types = [DeliveryStatus['by_' + nomail[2:]]]
    elif nomail == 'enabled':
        status_types = [DeliveryStatus.enabled]
    elif nomail == 'unknown':
        status_types = [DeliveryStatus.unknown]
    elif nomail == 'any':
        status_types = [
            DeliveryStatus.by_user,
            DeliveryStatus.by_bounces,
            DeliveryStatus.by_moderator,
            DeliveryStatus.unknown,
            ]
    else:                                           # pragma: nocover
        # click should enforce a valid nomail option.
        raise AssertionError(nomail)
    # Which roles should we display?
    if role is None:
        # By default, filter on members.
        roster = mlist.members
    elif role == 'administrator':
        roster = mlist.administrators
    elif role == 'any':
        roster = mlist.subscribers
    else:
        # click should enforce a valid member role.
        roster = mlist.get_roster(MemberRole[role])
    # Print; outfp will be either the file or stdout to print to.
    addresses = list(roster.addresses)
    if len(addresses) == 0:
        print(_('$mlist.list_id has no members'), file=outfp)
        return
    for address in sorted(addresses, key=attrgetter('email')):
        if regular:
            member = roster.get_member(address.email)
            if member.delivery_mode != DeliveryMode.regular:
                continue
        if digest is not None:
            member = roster.get_member(address.email)
            if member.delivery_mode not in digest_types:
                continue
        if nomail is not None:
            member = roster.get_member(address.email)
            if member.delivery_status not in status_types:
                continue
        print(formataddr((address.display_name, address.original_email)),
              file=outfp)


@transactional
def add_members(mlist, add_infp):
    for line in add_infp:
        # Ignore blank lines and lines that start with a '#'.
        if line.startswith('#') or len(line.strip()) == 0:
            continue
        # Parse the line and ensure that the values are unicodes.
        display_name, email = parseaddr(line)
        if email == '':                                       # pragma: nocover
            line = line.strip()                               # pragma: nocover
            print(_('Cannot parse as valid email address (skipping): $line'),
                  file=sys.stderr)                            # pragma: nocover
            continue                                          # pragma: nocover
        try:
            add_member(mlist,
                       RequestRecord(email, display_name,
                                     DeliveryMode.regular,
                                     mlist.preferred_language.code))
        except InvalidEmailAddressError:
            # It's okay if the address is invalid, we print a warning and
            # continue.
            line = line.strip()
            print(_('Cannot parse as valid email address (skipping): $line'),
                  file=sys.stderr)
        except AlreadySubscribedError:
            # It's okay if the address is already subscribed, just print a
            # warning and continue.
            if not display_name:
                print(_('Already subscribed (skipping): $email'),
                      file=sys.stderr)
            else:
                print(_('Already subscribed (skipping): $display_name <$email>'
                        ), file=sys.stderr)


@transactional
def delete_members(mlist, del_infp):
    for line in del_infp:
        # Ignore blank lines and lines that start with a '#'.
        if line.startswith('#') or len(line.strip()) == 0:
            continue
        # Parse the line and ensure that the values are unicodes.
        display_name, email = parseaddr(line)
        try:
            delete_member(mlist, email)
        except NotAMemberError:
            # It's okay if the address is not subscribed, just print a
            # warning and continue.
            if not display_name:
                print(_('Member not subscribed (skipping): $email'))
            else:
                print(_('Member not subscribed (skipping): '
                        '$display_name <$email>'))


@click.command(
    cls=I18nCommand,
    help=_("""\
    Display, add or delete a mailing list's members.
    Filtering along various criteria can be done when displaying.
    With no options given, displaying mailing list members
    to stdout is the default mode.
    """))
@click.option(
    '--add', '-a', 'add_infp', metavar='FILENAME',
    type=click.File(encoding='utf-8'),
    help=_("""\
    [MODE] Add all member addresses in FILENAME.  FILENAME can be '-' to
    indicate standard input.  Blank lines and lines that start with a
    '#' are ignored."""))
@click.option(
    '--delete', '-x', 'del_infp', metavar='FILENAME',
    type=click.File(encoding='utf-8'),
    help=_("""\
    [MODE] Delete all member addresses found in FILENAME
    from the specified list. FILENAME can be '-' to indicate standard input.
    Blank lines and lines that start with a '#' are ignored."""))
@click.option(
    '--output', '-o', 'outfp', metavar='FILENAME',
    type=click.File(mode='w', encoding='utf-8', atomic=True),
    help=_("""\
    [MODE] Display output to FILENAME instead of stdout.  FILENAME
    can be '-' to indicate standard output."""))
@click.option(
    '--role', '-R',
    type=click.Choice(('any', 'owner', 'moderator', 'nonmember', 'member',
                       'administrator')),
    help=_("""\
    [output filter] Display only members with a given ROLE.
    The role may be 'any', 'member', 'nonmember', 'owner', 'moderator',
    or 'administrator' (i.e. owners and moderators).
    If not given, then delivery members are used. """))
@click.option(
    '--regular', '-r',
    is_flag=True, default=False,
    help=_("""\
    [output filter] Display only regular delivery members."""))
@click.option(
    '--digest', '-d', metavar='kind',
    # baw 2010-01-23 summary digests are not really supported yet.
    type=click.Choice(('any', 'plaintext', 'mime')),
    help=_("""\
    [output filter] Display only digest members of kind.
    'any' means any digest type, 'plaintext' means only plain text (rfc 1153)
    type digests, 'mime' means MIME type digests."""))
@click.option(
    '--nomail', '-n', metavar='WHY',
    type=click.Choice(('enabled', 'any', 'unknown',
                       'byadmin', 'byuser', 'bybounces')),
    help=_("""\
    [output filter] Display only members with a given delivery status.
    'enabled' means all members whose delivery is enabled, 'any' means
    members whose delivery is disabled for any reason, 'byuser' means
    that the member disabled their own delivery, 'bybounces' means that
    delivery was disabled by the automated bounce processor,
    'byadmin' means delivery was disabled by the list
    administrator or moderator, and 'unknown' means that delivery was disabled
    for unknown (legacy) reasons."""))
@click.argument('listspec')
@click.pass_context
def members(ctx, add_infp, del_infp, outfp,
            role, regular, digest, nomail, listspec):
    mlist = getUtility(IListManager).get(listspec)
    if mlist is None:
        ctx.fail(_('No such list: $listspec'))
    if add_infp is not None:
        add_members(mlist, add_infp)
    elif del_infp is not None:
        delete_members(mlist, del_infp)
    else:
        display_members(ctx, mlist, role, regular, digest, nomail, outfp)


@public
@implementer(ICLISubCommand)
class Members:
    name = 'members'
    command = members
