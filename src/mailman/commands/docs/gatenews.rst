=====================================
Poll the NNTP Server For New Messages
=====================================

The ``mailman gate_news`` command is normally run periodically, usually a few
times per hour, by cron to pole the configured NNTP server for new messages to
be posted to lists that are configured to gateway messages from a usenet group.

There are no options other than ``--help``.
::

    >>> command = cli('mailman.commands.cli_gatenews.gatenews')

    >>> command('mailman gatenews --help')
    Usage: gatenews [OPTIONS]
    <BLANKLINE>
      Poll the NNTP server for messages to be gatewayed to mailing lists.
    <BLANKLINE>
    Options:
      --help  Show this message and exit.
