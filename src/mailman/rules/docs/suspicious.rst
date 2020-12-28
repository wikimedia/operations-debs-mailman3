==================
Suspicious headers
==================

Suspicious headers are a way for Mailman to hold messages that match a
particular regular expression.  This mostly historical feature is fairly
confusing to users, and the list attribute that controls this is misnamed.

    >>> from mailman.app.lifecycle import create_list
    >>> mlist = create_list('_xtest@example.com')
    >>> from mailman.config import config    
    >>> rule = config.rules['suspicious-header']
    >>> print(rule.name)
    suspicious-header

Set the so-called suspicious header configuration variable.

    >>> mlist.bounce_matching_headers = 'From: .*person@(blah.)?example.com'
    >>> from mailman.testing.helpers import (specialized_message_from_string
    ...   as message_from_string)    
    >>> msg = message_from_string("""\
    ... From: aperson@example.com
    ... To: _xtest@example.com
    ... Subject: An implicit message
    ... 
    ... """)
    >>> rule.check(mlist, msg, {})
    True

But if the header doesn't match the regular expression, the rule won't match.
This one comes from a ``.org`` address.

    >>> msg = message_from_string("""\
    ... From: aperson@example.org
    ... To: _xtest@example.com
    ... Subject: An implicit message
    ... 
    ... """)
    >>> rule.check(mlist, msg, {})
    False
