# /etc/cron.d/mailman3: crontab entries for the mailman3 package

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

0 0 * * *	list	if [ -x /usr/bin/mailman ]; then /usr/bin/mailman digests --send; fi
