Þ    )      d  ;   ¬        ¿     Y   Y  _   ³  â       ö  ß    {   e
     á
  .   ð
  -     /   M  <   }     º  <   Ç  &        +     H  !   g  #        ­  M   ¾  =     O   J       )   «      Õ  +   ö  0   "  ,   S  0     .   ±  e   à     F     c  ;   z  D   ¶  >   û  !   :     \     n  Ö      c  Y   s  _   Í  â  -       ß    {        û  H     0   Y  C     M   Î       <   .  2   k  '        Æ  4   å  0        K  U   a  X   ·  j        {  =         Ñ  B   ò  0   5  ;   f  C   ¢  .   æ       '        ¾  R   Ý  J   0   M   {   -   É      ÷   ½   !                 
   '   "          &   !   	                                                                              %          )                                       (   #                $                  Configuration file to use.  If not given, the environment variable
    MAILMAN_CONFIG_FILE is consulted and used if set.  If neither are given, a
    default configuration file is loaded.     Don't print status messages.  Error messages are still printed to standard
    error.     File to send the output to.  If not given, or if '-' is given, standard
    output is used.     If the master watcher finds an existing master lock, it will normally exit
    with an error message.  With this option, the master will perform an extra
    level of checking.  If a process matching the host/pid described in the
    lock file is running, the master will still exit, requiring you to manually
    clean up the lock.  But if no matching process is found, the master will
    remove the apparently stale lock and make another attempt to claim the
    master lock.     Key to use for the lookup.  If no section is given, all the key-values pair
    from any section matching the given key will be displayed.     Normally, this script will refuse to run if the user id and group id are
    not set to the 'mailman' user and group (as defined when you configured
    Mailman).  If run as root, this script will change to this user and group
    before the check is made.

    This can be inconvenient for testing and debugging purposes, so the -u flag
    means that the step that sets and checks the uid/gid is skipped, and the
    program is run as the current user and group.  This flag is not recommended
    for normal production environments.

    Note though, that if you run with -u and are not in the mailman group, you
    may have permission problems, such as being unable to delete a list's
    archives through the web.  Tough luck!     Section to use for the lookup.  If no key is given, all the key-value pairs
    of the given section will be displayed.  (Digest mode) $mlist.display_name mailing list probe message $mlist.display_name subscription notification $mlist.display_name unsubscription notification $mlist.fqdn_listname post from $msg.sender requires approval (no subject) An alternative directory to output the various MTA files to. Discard a message and stop processing. Forward of moderated message GNU Mailman is already running Header "{}" matched a header rule Hold a message and stop processing. Moderation chain New subscription request to $self.mlist.display_name from $self.address.email New unsubscription request from $mlist.display_name by $email New unsubscription request to $self.mlist.display_name from $self.address.email Original Message Posting of your message titled "$subject" Print the Mailman configuration. Process DMARC reject or discard mitigations Regenerate the aliases appropriate for your MTA. Reject/bounce a message and stop processing. Request to mailing list "$display_name" rejected Start the Mailman master and runner processes. The master lock could not be acquired because it appears as though another
master is already running. Uncaught bounce notification Unsubscription request Welcome to the "$mlist.display_name" mailing list${digmode} You have been unsubscribed from the $mlist.display_name mailing list Your message to $mlist.fqdn_listname awaits moderator approval [No bounce details are available] [No reason given] list:user:notice:rejected.txt Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2020-04-10 11:11+0000
Last-Translator: Yaron Shahrabani <sh.yaron@gmail.com>
Language-Team: Hebrew <https://hosted.weblate.org/projects/gnu-mailman/mailman/he/>
Language: he
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=4; plural=(n == 1) ? 0 : ((n == 2) ? 1 : ((n > 10 && n % 10 == 0) ? 2 : 3));
X-Generator: Weblate 4.0-dev
     ×§×××¥ ××××¨××ª ××©××××©.  ×× ×× ×¦×××, ×××××¨××ª ×©×××¤××¢××ª ×××©×ª× × ××¡××××ª×
    MAILMAN_CONFIG_FILE ×ª×××× × ××¤×¢××××ª.  ×× ×× ×¦××× × ××£ ×××ª ×××,
    ×××¢× ×§×××¥ ××××¨××ª ×××¨×¨×ª ××××.     Don't print status messages.  Error messages are still printed to standard
    error.     File to send the output to.  If not given, or if '-' is given, standard
    output is used.     If the master watcher finds an existing master lock, it will normally exit
    with an error message.  With this option, the master will perform an extra
    level of checking.  If a process matching the host/pid described in the
    lock file is running, the master will still exit, requiring you to manually
    clean up the lock.  But if no matching process is found, the master will
    remove the apparently stale lock and make another attempt to claim the
    master lock.     Key to use for the lookup.  If no section is given, all the key-values pair
    from any section matching the given key will be displayed.     Normally, this script will refuse to run if the user id and group id are
    not set to the 'mailman' user and group (as defined when you configured
    Mailman).  If run as root, this script will change to this user and group
    before the check is made.

    This can be inconvenient for testing and debugging purposes, so the -u flag
    means that the step that sets and checks the uid/gid is skipped, and the
    program is run as the current user and group.  This flag is not recommended
    for normal production environments.

    Note though, that if you run with -u and are not in the mailman group, you
    may have permission problems, such as being unable to delete a list's
    archives through the web.  Tough luck!     Section to use for the lookup.  If no key is given, all the key-value pairs
    of the given section will be displayed.  (××¦× ×ª×§×¦××¨) ××××¢×ª ×ª×©××× ××× ×¨×©×××ª ××××××¨ $mlist.display_name ××××¢×ª ××× ×× ××× $mlist.display_name ××××¢×ª ××××× ××× ×× ×××¨×©××× $mlist.display_name ××¤×¨×¡×× ×©× $mlist.fqdn_listname ×××ª $msg.sender ×××¨×© ×××©××¨ (××× × ××©×) An alternative directory to output the various MTA files to. ××©×××ª ×××××¢× ××¢×¦××¨×ª ××¢××××. ××¢××¨× ×©× ××××¢× ××¤××§××ª GNU Mailman is already running ××××ª×¨×ª â{}â ×ª××××ª ×××× ×××ª×¨×ª ××××§×ª ××××¢× ×××¤×¡×§×ª ××¢××××. ×©×¨×©×¨×ª ×¤××§×× ××§×©×ª ××× ×× ×××©× ×× $self.mlist.display_name ×××ª $self.address.email ××§×©×ª ××××× ××× ×× ×××©× ×××¨×©××× $mlist.display_name ×××ª $email ××§×©×ª ××××× ××× ×× ×××©× ×××¨×©××× $self.mlist.display_name ×××ª $self.address.email ××××¢× ××§××¨××ª ×¤×¨×¡×× ×××××¢× ×©×× ×¢× ×× ××©× â$subjectâ Print the Mailman configuration. ×¢×××× ×××××ª DMARC ×× ××ª×¢××××ª ××××¤×××ª×× Regenerate the aliases appropriate for your MTA. ×××××ª/××§×¤×¦×ª ××××¢× ×××¤×¡×§×ª ××¢××××. ×××§×©× ××¨×©×××ª ××××××¨ â$display_nameâ × ×××ª× Start the Mailman master and runner processes. ×× × ××ª× ×××©×× ××ª ×× ×¢××× ××¨××©××ª ××××× ×©× ×¨×× ×©××© ×××¨ ×©××¨××ª
×××¨× ×××¨ ××××. ××××¢×ª ××××¨× ×©×× × ×ª×¤×¡× ××§×©×ª ××××× ××× ×× ××¨×× ×××× ×× ×¨×©×××ª ××××××¨ â$mlist.display_nameâ${digmode} ×××× ×× ×©×× ××¨×©×××ª ××××××¨ $mlist.display_name ×××× ××××¢×ª× ×× $mlist.fqdn_listname ×××ª×× × ××××©××¨ ××¤××§×× [×¤×¨×× ×××××¨× ××× × ×××× ××] [×× ×¡××¤×§× ×¡×××] ××××¢×ª× ××¨×©×××ª ××××××¨ $listname × ×××ª× ×××¡××××ª ×××××ª:$reasons ×××××¢× ×××§××¨××ª ×©××ª×§××× ×¢× ××× Mailman ××¦××¨×¤×ª ×××××¢× ××. 