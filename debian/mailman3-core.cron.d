# /etc/cron.d/mailman3-core: crontab entries for the mailman3-core package

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

0 0 * * *	list	if [ -x /usr/bin/mailman ]; then /usr/bin/mailman digests --send; fi