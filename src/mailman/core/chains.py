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

"""Application support for chain processing."""

from mailman.config import config
from mailman.interfaces.chain import IChain, LinkAction
from mailman.utilities.modules import add_components
from public import public


@public
def process(mlist, msg, msgdata, start_chain='default-posting-chain'):
    """Process the message through a chain.

    :param mlist: the IMailingList for this message.
    :param msg: The Message object.
    :param msgdata: The message metadata dictionary.
    :param start_chain: The name of the chain to start the processing with.
    """
    # Set up some bookkeeping.
    chain_stack = []
    msgdata['rule_hits'] = hits = []
    msgdata['rule_misses'] = misses = []
    # Find the starting chain and begin iterating through its links.
    chain = config.chains[start_chain]
    chain_iter = chain.get_links(mlist, msg, msgdata)
    # Loop until we've reached the end of all processing chains.
    while chain:
        # Iterate over all links in the chain.  Do this outside a for-loop so
        # we can capture a chain's link iterator in mid-flight.  This supports
        # the 'detour' link action.
        try:
            link = next(chain_iter)
        except StopIteration:
            # This chain is exhausted.  Pop the last chain on the stack and
            # continue iterating through it.  If there's nothing left on the
            # chain stack then we're completely finished processing.
            if len(chain_stack) == 0:
                return
            chain, chain_iter = chain_stack.pop()
            continue
        if link.rule.check(mlist, msg, msgdata):
            if link.rule.record:
                hits.append(link.rule.name)
            # The rule matched so run its action.
            if link.action is LinkAction.jump:
                chain = link.chain
                chain_iter = chain.get_links(mlist, msg, msgdata)
                continue
            elif link.action is LinkAction.detour:
                # Push the current chain so that we can return to it when
                # the next chain is finished.
                chain_stack.append((chain, chain_iter))
                chain = link.chain
                chain_iter = chain.get_links(mlist, msg, msgdata)
                continue
            elif link.action is LinkAction.stop:
                # Stop all processing.
                return
            elif link.action is LinkAction.defer:
                # Just process the next link in the chain.
                pass
            elif link.action is LinkAction.run:
                link.function(mlist, msg, msgdata)
            else:
                raise AssertionError(
                    'Bad link action: {}'.format(link.action))
        else:
            # The rule did not match; keep going.
            if link.rule.record:
                misses.append(link.rule.name)


@public
def initialize():
    """Set up chains, both built-in and from the database."""
    add_components('chains', IChain, config.chains)
