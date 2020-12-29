# /etc/cron.d/mailman3: crontab entries for the mailman3 package

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# At 8AM, send out notifices of pending requests to list moderators
0  8 * * *  list	if [ -x /usr/bin/mailman ]; then /usr/bin/mailman notify; fi

# At 12AM, send mail digests for lists that do periodic as well as threshold delivery
0 12 * * *  list	if [ -x /usr/bin/mailman ]; then /usr/bin/mailman digests --periodic; fi

# Every 15 minutes, gate messages from usenet to those lists which have the gateway configured
*/15 * * * *   list    if [ -x /usr/bin/mailman ]; then /usr/bin/mailman gatenews; fi
