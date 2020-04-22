��    �      �  �         �  a  �  T     �   h  ^   (  Y   �  o   �  _   Q  G   �  �  �  �  �  �   �  �   K  �   �    �  �  �  P   �   �   �   �   �!  �   �"  {   f#  b   �#  ^   E$  �  �$     D'  $   S'  K   x'  6   �'  .   �'  -   *(  /   X(  <   �(  Q   �(     )  M   5)  L   �)     �)  0   �)  !   *  :   9*  *   t*  4   �*     �*  3   �*  K   +     a+     s+     �+     �+  <   �+  (   �+     ,  "   8,  	   [,  *   e,  &   �,     �,  3   �,  x   -     -     �-  ?   �-     �-  )   .  (   @.  !   i.  #   �.  m  �.     0  !   <0  !   ^0  (   �0  9   �0  %   �0  +   	1  '   51     ]1     y1  (   �1     �1  C   �1     2     &2  #   >2  :   b2  )   �2     �2     �2  M   �2  =   *3  O   h3     �3     �3     �3     4     "4     <4     T4  2   j4  2   �4  6   �4     5     5  #   ,5  C   P5  )   �5     �5     �5      �5  +   6     <6  0   I6  !   z6  ,   �6     �6     �6  0   �6     /7  $   N7     s7  2   7     �7     �7  6   �7      "8  %   C8  8   i8     �8  .   �8      �8  1   
9  -   <9     j9     w9  "   �9  "   �9     �9  e   �9    [:  �   o;  /   �;     *<     G<     a<     ~<  	   �<  ;   �<  D   �<  >    =  %   _=  J   �=  !   �=     �=     >      >     =>  /   F>     v>     �>  !   �>     �>  "   �>  !   ?     8?     X?     w?      �?     �?  "   �?     �?     @     )@     E@     c@     �@  �  �@  �  B  _   �D  �   IE  O   =F  x   �F  �   G  t   �G  W   H  I  hH  u  �J  �   (M  �   �M  �   �N  �  XO  �  T  r   �W    rX    {Y  �   �Z  �   s[  |   
\  w   �\  
  �\     
`  9   `  I   T`  E   �`  <   �`  0   !a  2   Ra  H   �a  R   �a  #   !b  O   Eb  U   �b     �b  8   c  &   >c  A   ec  :   �c  7   �c     d  E   'd  m   md     �d     �d     e     "e  C   =e  ;   �e  %   �e  +   �e  	   f  1   f  -   Kf  '   yf  H   �f  �   �f     �g     �g  A   �g  /   h  ;   5h  L   qh  8   �h  +   �h  �  #i  %   �j  +   �j  1   k  +   ?k  E   kk  *   �k  ;   �k  -   l  0   Fl  +   wl  ?   �l  !   �l  `   m     fm  '   tm  '   �m  G   �m  3   n     @n  
   Wn  \   bn  E   �n  \   o      bo  /   �o  ;   �o  (   �o  &   p     ?p     ^p  C   yp  M   �p  >   q     Jq     cq  %   tq  U   �q  1   �q     "r  )   >r  %   hr  8   �r     �r  8   �r  +   s  3   :s  !   ns     �s  <   �s     �s  5   t     At  9   St  (   �t      �t  @   �t  &   u  '   ?u  C   gu     �u  8   �u  $   v  0   &v  .   Wv     �v     �v  )   �v  5   �v  &   w  t   6w  C  �w  �   �x  ;   �y  &   �y     �y  $   	z     .z     Iz  C   [z  I   �z  K   �z  2   5{  I   h{  0   �{     �{     |  �   |  P  �}  :   .�  B  i�  u   ��  x   "�  9   ��    Ճ  ,   �  �  �  �   ��  �  [�  �  ��    ��    ��  k   ��  �  ,�    �  �   �    ��     (�     e   �          �   .       $          o   u       k         >   [   �   {       �   \   C   Q   h               X   c      m   1       N      H   �       �   6   ?   U   �   �      T       �   �   x       �           l       �   �          %   ^   �   y   Z   S   �   t           f       �              D   ;      7   n      9   �      �              �   -       �         |   g   '           &      W          O   ~       �      
       }   �   �               �   @       G   j   /   0   p       A   �   (       �   �   P   2       L   	   E          w   ]   R          �   �   ,   �   !                  #   �      B   _   Y       `   �       �   �       z   r   M       J          8               �           �   <         �       *   �   V   �       �       d   q       F   )   +   s   �   "   I   v   3       b   =   �   :   �       5      �   a       4      K   i   �   �       �         �    
    Start the named runner, which must be one of the strings returned by the -l
    option.

    For runners that manage a queue directory, optional `slice:range` if given
    is used to assign multiple runner processes to that queue.  range is the
    total number of runners for the queue while slice is the number of this
    runner from [0..range).  For runners that do not manage a queue, slice and
    range are ignored.

    When using the `slice:range` form, you must ensure that each runner for the
    queue is given the same range value.  If `slice:runner` is not given, then
    1:1 is used.
         A more verbose output including the file system paths that Mailman is
    using.     Configuration file to use.  If not given, the environment variable
    MAILMAN_CONFIG_FILE is consulted and used if set.  If neither are given, a
    default configuration file is loaded.     Don't actually do anything, but in conjunction with --verbose, show what
    would happen.     Don't print status messages.  Error messages are still printed to standard
    error.     Don't restart the runners when they exit because of an error or a SIGUSR1.
    Use this only for debugging.     File to send the output to.  If not given, or if '-' is given, standard
    output is used.     File to send the output to.  If not given, standard output is used.     If the master watcher finds an existing master lock, it will normally exit
    with an error message.  With this option, the master will perform an extra
    level of checking.  If a process matching the host/pid described in the
    lock file is running, the master will still exit, requiring you to manually
    clean up the lock.  But if no matching process is found, the master will
    remove the apparently stale lock and make another attempt to claim the
    master lock.     If the master watcher finds an existing master lock, it will normally exit
    with an error message.  With this option,the master will perform an extra
    level of checking.  If a process matching the host/pid described in the
    lock file is running, the master will still exit, requiring you to manually
    clean up the lock.  But if no matching process is found, the master will
    remove the apparently stale lock and make another attempt to claim the
    master lock.     Import Mailman 2.1 list data'.  Requires the fully-qualified name of the
    list to import and the path to the Mailman 2.1 pickle file.     Increment the digest volume number and reset the digest number to one.  If
    given with --send, the volume number is incremented before any current
    digests are sent.     Key to use for the lookup.  If no section is given, all the key-values pair
    from any section matching the given key will be displayed.     Master subprocess watcher.

    Start and watch the configured runners, ensuring that they stay alive and
    kicking.  Each runner is forked and exec'd in turn, with the master waiting
    on their process ids.  When it detects a child runner has exited, it may
    restart it.

    The runners respond to SIGINT, SIGTERM, SIGUSR1 and SIGHUP.  SIGINT,
    SIGTERM and SIGUSR1 all cause a runner to exit cleanly.  The master will
    restart runners that have exited due to a SIGUSR1 or some kind of other
    exit condition (say because of an uncaught exception).  SIGHUP causes the
    master and the runners to close their log files, and reopen then upon the
    next printed message.

    The master also responds to SIGINT, SIGTERM, SIGUSR1 and SIGHUP, which it
    simply passes on to the runners.  Note that the master will close and
    reopen its own log files on receipt of a SIGHUP.  The master also leaves
    its own process id in the file specified in the configuration file but you
    normally don't need to use this PID directly.     Normally, this script will refuse to run if the user id and group id are
    not set to the 'mailman' user and group (as defined when you configured
    Mailman).  If run as root, this script will change to this user and group
    before the check is made.

    This can be inconvenient for testing and debugging purposes, so the -u flag
    means that the step that sets and checks the uid/gid is skipped, and the
    program is run as the current user and group.  This flag is not recommended
    for normal production environments.

    Note though, that if you run with -u and are not in the mailman group, you
    may have permission problems, such as being unable to delete a list's
    archives through the web.  Tough luck!     Notify the list owner by email that their mailing list has been
    created.     Operate on this mailing list.  Multiple --list options can be given.  The
    argument can either be a List-ID or a fully qualified list name.  Without
    this option, operate on the digests for all mailing lists.     Override the default set of runners that the master will invoke, which is
    typically defined in the configuration file.  Multiple -r options may be
    given.  The values for -r are passed straight through to bin/runner.     Run the named runner exactly once through its main loop.  Otherwise, the
    runner runs indefinitely until the process receives a signal.  This is not
    compatible with runners that cannot be run once.     Section to use for the lookup.  If no key is given, all the key-value pairs
    of the given section will be displayed.     Send any collected digests for the List only if their digest_send_periodic
    is set to True.     Send any collected digests right now, even if the size threshold has not
    yet been met.     Start a runner.

    The runner named on the command line is started, and it can either run
    through its main loop once (for those runners that support this) or
    continuously.  The latter is how the master runner starts all its
    subprocesses.

    -r is required unless -l or -h is given, and its argument must be one of
    the names displayed by the -l switch.

    Normally, this script should be started from `mailman start`.  Running it
    separately or with -o is generally useful only for debugging.  When run
    this way, the environment variable $MAILMAN_UNDER_MASTER_CONTROL will be
    set which subtly changes some error handling behavior.
      (Digest mode) $count matching mailing lists found: $member unsubscribed from ${mlist.display_name} mailing list due to bounces $member's subscription disabled on $mlist.display_name $mlist.display_name mailing list probe message $mlist.display_name subscription notification $mlist.display_name unsubscription notification $mlist.fqdn_listname post from $msg.sender requires approval $mlist.list_id bumped to volume $mlist.volume, number ${mlist.next_digest_number} $mlist.list_id has no members $mlist.list_id is at volume $mlist.volume, number ${mlist.next_digest_number} $mlist.list_id sent volume $mlist.volume, number ${mlist.next_digest_number} $name runs $classname $person has a pending subscription for $listname $person left $mlist.fqdn_listname $self.name: $email is not a member of $mlist.fqdn_listname $self.name: no such command: $command_name $self.name: too many arguments: $printable_arguments (no subject) --send and --periodic flags cannot be used together A previous run of GNU Mailman did not exit cleanly ({}).  Try using --force Accept a message. An alias for 'end'. An alias for 'join'. An alias for 'leave'. An alternative directory to output the various MTA files to. Cannot import runner module: $class_path Confirm a subscription request. Confirmation email sent to $person Confirmed Created mailing list: $mlist.fqdn_listname Discard a message and stop processing. Display Mailman's version. Display more debugging information to the log file. For unknown reasons, the master lock could not be acquired.

Lock file: $config.LOCK_FILE
Lock host: $hostname

Exiting. Forward of moderated message GNU Mailman is already running GNU Mailman is in an unexpected state ($hostname != $fqdn_name) GNU Mailman is not running GNU Mailman is running (master pid: $pid) Get help about available email commands. Header "{}" matched a header rule Hold a message and stop processing. If you reply to this message, keeping the Subject: header intact, Mailman will
discard the held message.  Do this if the message is spam.  If you reply to
this message and include an Approved: header with the list password in it, the
message will be approved for posting to the list.  The Approved: header can
also appear in the first line of the body of the reply. Ignoring non-dictionary: {0!r} Illegal list name: $fqdn_listname Illegal owner addresses: $invalid Information about this Mailman instance. Inject a message from a file into a mailing list's queue. Invalid language code: $language_code Invalid or unverified email address: $email Invalid value for [shell]use_python: {} Is the master even running? Join this mailing list. Last autoresponse notification for today Leave this mailing list. Leave this mailing list.

You may be asked to confirm your request. Less verbosity List all mailing lists. List already exists: $fqdn_listname List only those mailing lists that are publicly advertised List the available runner names and exit. Moderation chain N/A New subscription request to $self.mlist.display_name from $self.address.email New unsubscription request from $mlist.display_name by $email New unsubscription request to $self.mlist.display_name from $self.address.email No child with pid: $pid No confirmation token found No matching mailing lists found No runner name given. No such list found: $spec No such list: $listspec No such queue: $queue Not a Mailman 2.1 configuration file: $pickle_file Notify list owners/moderators of pending requests. Number of objects found (see the variable 'm'): $count Operate on digests. Original Message PID unreadable in: $config.PID_FILE Poll the NNTP server for messages to be gatewayed to mailing lists. Posting of your message titled "$subject" Print less output. Print some additional status. Print the Mailman configuration. Process DMARC reject or discard mitigations Reason: {}

 Regenerate the aliases appropriate for your MTA. Regular expression requires --run Reject/bounce a message and stop processing. Remove a mailing list. Reopening the Mailman runners Request to mailing list "$display_name" rejected Restarting the Mailman runners Send an acknowledgment of a posting. Sender: {}
 Show a list of all available queue names and exit. Show also the list descriptions Show also the list names Show the current running status of the Mailman system. Show this help message and exit. Shutting down Mailman's master runner Signal the Mailman processes to re-open their log files. Stale pid file removed. Start the Mailman master and runner processes. Starting Mailman's master runner Stop and restart the Mailman runner subprocesses. Stop the Mailman master and runner processes. Subject: {}
 Suppress status messages The built-in -owner posting chain. The built-in header matching chain The built-in moderation chain. The master lock could not be acquired because it appears as though another
master is already running. The master lock could not be acquired, because it appears as if some process
on some other host may have acquired it.  We can't test for stale locks across
host boundaries, so you'll have to clean this up manually.

Lock file: $config.LOCK_FILE
Lock host: $hostname

Exiting. The master lock could not be acquired.  It appears as though there is a stale
master lock.  Try re-running $program with the --force flag. The {} list has {} moderation requests waiting. Uncaught bounce notification Undefined domain: $domain Undefined runner name: $name Unsubscription request User: {}
 Welcome to the "$mlist.display_name" mailing list${digmode} You have been unsubscribed from the $mlist.display_name mailing list Your message to $mlist.fqdn_listname awaits moderator approval Your new mailing list: $fqdn_listname Your subscription for ${mlist.display_name} mailing list has been disabled [No bounce details are available] [No reason given] bad argument: $argument domain:admin:notice:new-list.txt help.txt ipython is not available, set use_ipython to no list:admin:action:post.txt list:admin:action:subscribe.txt list:admin:action:unsubscribe.txt list:admin:notice:subscribe.txt list:admin:notice:unrecognized.txt list:admin:notice:unsubscribe.txt list:member:digest:masthead.txt list:member:generic:footer.txt list:user:action:subscribe.txt list:user:action:unsubscribe.txt list:user:notice:hold.txt list:user:notice:no-more-today.txt list:user:notice:post.txt list:user:notice:probe.txt list:user:notice:refuse.txt list:user:notice:rejected.txt list:user:notice:welcome.txt n/a Project-Id-Version: mm 3
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2020-04-17 04:35+0000
Last-Translator: anonymous <noreply@weblate.org>
Language-Team: French <https://hosted.weblate.org/projects/gnu-mailman/mailman/fr/>
Language: fr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n > 1;
X-Generator: Weblate 4.0.1-dev
 
    Lance le processus nommé, qui doit être une des chaînes retournées par
    l'option -l.

    Pour les processus qui gèrent un répertoire de queue, l'optionnel
    « part:intervalle », si utilisé, sert à affecter plusieurs processus à cette queue.
    « intervalle » est le nombre total de processus pour la queue tandis que
    « part » est le numéro de ce processus dans [0..range). Pour les processus
    qui ne gèrent pas une queue, « part » et « intevalle » sont ignorés.

    En utilisant la forme « part:intervalle », vous devez vous assurer que chaque
    processus pour la queu reçoit la même valeur d'intervalle. Si « part:intervalle »
    n'est pas fourni, alors 1:1 est utilisé.
         Une sortie plus prolixe incluant les chemins système des fichiers que
    Mailman utilise.     Fichier de configuration ) utiliser.  S'il n'est pas fourni, la variable d'environnement
    MAILMAN_CONFIG_FILE est lue et utilisée si définie. Si ni l'un ni l'autre sont fournis, un
    fichier de configuration par défaut est chargé.     Ne fait rien, mais en conjonction de --verbose, montre ce qui se passerait.     Ne communique pas les messages d'état. Les messages d'erreur restent
    envoyés vers la sortie d'erreur standard.     Ne relance pas les processus quand ils se terminent à cause d'une erreur ou d'un SIGUSR1.
    N'utiliser que pour la mise au point du logiciel.     Fichier vers lequel envoyer la sortie. Si absent ou si « - » est fourni,
    la sortie standard est utilisée.     Fichier vers lequel envoyer la sortie. Si absent, la sortie standard est utilisée.     Si le surveillant pilote trouve un verrou principal, il se terminera
    normalement avec un message d'erreur. Avec cette option, le pilote
    effectuera un niveau supplémentaire de vérifications. Si un
    processus correspondant au serveur/pid indiqué dans le fichier
    verrou est en cours d'exécution, le pilote se terminera toujours en 
    vous demandant de supprimer manuellement le verrou. Mais si aucun
    processus correspondant n'est trouvé, le pilote supprimera le verrou
    apparemment caduc et effectuera une autre tentative de poser le
    verrou principal.     Si le pilote de surveillance trouve un verrou principal déjà existant, il va
    normalement se terminer avec un message d'erreur. Avec cette option,
    le pilote va effectuer un niveau de vérification supplémentaire. Si un
    processus avec le serveur/pid correspondant à celui donné dans le
    fichier verrou est déjà en opération, le pilote va toujours se terminer,
    en vous demandant de supprimer manuellement le verrou. Mais si
    aucun processus correspondant n'est trouvé, le pilote va supprimer
    le verrou apparemment oublié et effectuer une nouvelle tentative 
    d'obtenir le verrou principal.     Importer les données de liste Mailman 2.1. Nécessite le  nom pleinement
    qualifié de la liste à importer et le chemin vers le fichier conserve de
    Mailman 2.1.     Incrémente le numéro de volume du condensé et remets le numéro de
    condensé à un. Si accompagné de --send, le numéro de volume est
    incrémenté avant tout envoi de condensé en cours.     Clef à utiliser pour la consultation. Si aucune section n'est donnée, toutes
    les paires clef-valeur de toute section correspondant à la clef donnée
    seront affichées.     Pilote de surveillance des processus.

    Lance et surveille les processus configurés, vérifiant qu'ils tournent et 
    restent réactifs. Chaque processus est engendré et exécuté à son tour,
    tandis que le pilote surveille leur identifiant (PID). Quand il détecte qu'un
    processus fils s'est terminé, il peut le relancer.

    Les processus répondent à SIGINT, SIGTERM, SIGUSR1 et SIGHUP.  SIGINT,
    SIGTERM et SIGUSR1 provoquent tous une fin propre du processus. Le
    pilote va redémarrer les processus qui se sont terminés à cause d'un
    SIGUSR1 ou tout autre raison d'interruption (par exemple à cause d'une
    erreur non-gérée). SIGHUP oblige le pilote et les processus à fermer leur
    fichiers de journaux et à les réouvrir au prochain message enregistré.

    Le pilote répond aussi à SIGINT, SIGTERM, SIGUSR1 et SIGHUP, qu'il
    transmet simplement aux processus. Notez que le pilote va fermer et
    réouvrir son propre fichier journal à la réception d'un SIGHUP. Le pilote
    laisse aussi son propre identifiant de processus dans le fichier spécifié
    dans le fichier de configuration mais vous n'avez normalement pas
    besoin d'utiliser ce PID directement.     Normalement cette procédure refusera de s'exécuter si l'identifiant
    utilisateur et l'identifiant de group ne sont pas respectivement
    positionnés à l'utilisateur « mailman » et le groupe (comme défini
    lorsque vous avez configuré Mailman).  Si exécuté en tant que « root »,
    cette procédure s'incarnera en cet utilisateur et ce groupe avant que la
    vérification soit faite.

    Cela peut être désagréable dans des circonstances de tests et d'analyse
    donc l'option -u signifie que l'étape qui positionne et vérifie les uid/gid
    est sautée et que le programme est exécuté comme l'utilisateur et le
    groupe courants. Cette option n'est pas recommandée dans des
    environnements de production normaux.

    Notez cependant que, si vous exécutez avec -u et n'êtes pas dans le
    groups mailman, vous pouvez avoir des problèmes de droits, comme
    être incapable de supprimer les les archives d'une liste par l'interface.
    Tant pis !     Informer le propriétaire de la liste par courrier électronique que sa liste de diffusion a été
    créé.     Agit sur cette liste de diffusion. De multiples options --list peuvent être
    indiquées. L'argument peut soit être une List-ID ou un nom de liste
    pleinement qualifié. Sans cette option, agit sur les condensés pour
    toutes les listes de diffusion.     Remplace le jeu de processus que le pilote va lancer par défaut, qui est
    usuellement défini dans le fichier de configuration. De multiples
    options -r peuvent être données. Les valeurs pour -r sont transmises
    directement au processus bin/runner.     Exécute exactement une fois le parcours principal du processus nommé.
    Sinon, le processus s'exécute infiniment jusqu'à ce qu'il reçoive un signal.
    Incompatible avec les processus qui ne peuvent s'exécuter une seule fois.     Section à utiliser pour la consultation. Si aucune clef n'est donnée, toutes
    les paires clef-valeur de la section donnée seront affichées.     Expédie tout condensat collecté pour la liste seulement si son
    digest_send_periodic est positionné à « Vrai ».     Expédie tous les condensés collectés immédiatement, même si la taille
    seuil n'a pas encore été atteinte.     Lance un processus.

    Le processus nommé en ligne de commande est lancé et il peut soit
    s'exécuter une fois (pour ceux des processus qui en sont capables) ou
    en continu. La seconde est la façon dont le processus pilote démarre
    tous ses sous-processus.

    -r est nécessaire à moins que -l ou -h soit donnes et son argument doit
    être un des noms affichés par le sélecteur -l.

    Normallement, ce script doit être lancé depuis « mailman start ». Le
    lancer séparément ou avec -o n'est en général utile que pour la mise au
    point. Quand il est lancé de cette façon, la variable d'environnement
    $MAILMAN_UNDER_MASTER_CONTROL sera activée ce qui modifie
    subtilement certains comportements dans la gestion des erreurs.
      (mode Aperçu) $count listes de diffusion correspondantes de trouvées : Vous avez été désinscrits de la liste de diffusion $mlist.display_name Nouvelle demande de désinscription de $mlist.display_name par $email $mlist.display_name message de test de la liste de diffusion Notification d'abonnement à $mlist.display_name $mlist.display_name notification de désabonnement Le message $mlist.fqdn_listname de $msg.sender nécessite une validation $mlist.list_id porté au volume $mlist.volume, numéro ${mlist.next_digest_number} $mlist.list_id n’a pas d'abonnés $mlist.list_id est au volume $mlist.volume, numéro ${mlist.next_digest_number} $mlist.list_id a envoyé le volume $mlist.volume, numéro ${mlist.next_digest_number} $name exécute $classname $person possède un abonnement en attente pour $listname $person a quitté $mlist.fqdn_listname $self.name : $email n’est pas un membre de $mlist.fqdn_listname $self.name : aucune de commande de ce type : $command_name $self.name : trop d’arguments : $arguments_printables Pas de sujet les options --send et --periodic ne peuvent être utilisées ensemble Une précédente exécution de GNU Mailman ne s'est pas terminée proprement ({}). Essayez d'utilisez --force Accepte un message. Un alias pour « end ». Un alias pour « join ». Un alias pour « leave ». Un répertoire alternatif pour déposer les divers fichiers de MTA. Import impossible de l'extension de processus : $class_path Confirmer une demande d’abonnement. Courriel de confirmation envoyé à $person Confirmé Liste de diffusion créée : $mlist.fqdn_listname Éliminer un message et cesser le traitement. Afficher la version du facteur Mailman. Enregistre plus d'informations de mise au point dans le fichier journal. Pour des raisons inconnues, le verrou principal n'a pu être posé.

Fichier verrou : $config.LOCK_FILE
Serveur verrouillant : $hostname

Fin d'exécution. Transfert du message modéré GNU Mailman s'exécute déjà GNU Mailman est dans un état inattendu ($hostname != $fqdn_name) GNU Mailman n’est pas en cours d’exécution GNU Mailman est en cours d’exécution (master pid : $pid) Obtenez de l’aide sur les commandes de courrier électronique disponibles. L'entête « {} » a correspondu à une règle d'entête Retenir un message et cesser le traitement. Si vous répondez à ce message en gardant l'entête Subject: header intacte,
Mailman éliminera le message retenu. Faites-le si le message est du pouriel.
Si vous répondez à ce message y incluez une entête Approved: avec dedans
le mot de passe de la liste, le message sera validé pour publication dans la
liste. L'entête Approved: peut aussi être présente en première ligne du corps
de la réponse. Ignorer, hors du dictionnaire : {0!r} Nom de liste non autorisé : $fqdn_listname Adresses de propriétaires incorrectes : $invalid Informations sur cette instance de Mailman. Insérer un message d'un fichier dans une file de liste de diffusion. Code de langue non valide : $language_code Adresse électronique non valide ou non vérifiée : $email Valeur non valide pour [shell]use_python : {} Le pilote est-il même en train de s'exécuter ? Inscrivez-vous à cette liste de diffusion. Dernière notification de réponse automatique pour aujourd'hui Quitter cette liste de diffusion. Quitter cette liste de diffusion.

Il vous sera peut-être demandé de confirmer votre requête. Moins prolixe Montrer toutes les listes de diffusion. La liste existe déjà : $fqdn_listname Montrer seulement les listes de diffusion dont l'existence est publiée Liste les noms de processus disponibles et termine. Chaîne de modération Sans objet Nouvelle demande d'inscription à $self.mlist.display_name de la part de $self.address.email Nouvelle demande de désinscription de $mlist.display_name par $email Nouvelle demande de désinscription à $mlist.display_name de la part de $self.address.email Aucun descendant avec pid : $pid Aucun jeton de confirmation n’a été trouvé Aucune liste de diffusion correspondante n'a été trouvée Aucun nom de processus n'a été donné. Aucune telle liste de trouvée : $spec Aucune telle liste : $listspec Aucune telle file : $queue N'est pas un fichier de configuration de Mailman 2.1 : $pickle_file Informer les propriétaires/modérateurs de la liste des demandes en attente. Nombre d’objets trouvés (voir la variable « m ») : $count Agit sur les condensés. Message original PID illisible dans : $config.PID_FILE Sonder le serveur NNTP pour des messages à transférer vers les listes de diffusion. Publication de votre message intitulé "$subject" Afficher moins de détails. Imprime certains états supplémentaires. Imprimer la configuration de Mailman. Traite les atténuations de rejets / éliminations DMARC Raison : {}

 Engendrer à nouveau les alias adéquats pour votre MTA. L’expression régulière nécessite --run Rejeter/refuser un message et cesser le traitement. Supprimer une liste de diffusion. Réouvrir les processus Mailman Requête pour la liste de diffusion "$display_name" rejetée Relance des processus Mailman Envoyer un accusé de réception d’une publication. Expéditeur : {}
 Afficher une liste de tous les noms de files et terminer. Montrer aussi les descriptions de listes Montrer aussi les noms de listes Afficher l’état de fonctionnement actuel du système Mailman. Montrer ce message d'aide et terminer. Clôture du processus pilote de Mailman Signifie au processus Mailman de réouvrir leurs fichiers journaux. Fichier pid caduc supprimé. Lance les processus de Mailman dont le processus pilote. Lance le processus pilote de Mailman Arrête et relance les (sous-)processus Mailman. Arrêter les processus Mailman dont le pilote. Sujet : {}
 Effacer les messages d'état La chaîne incorporée d'envoi à -owner. La chaîne incorporée de correspondance des entêtes La chaîne de modération incorporée. Le verrou principal n’a pas pu être posé car il semble qu’un autre pilote est 
déjà en cours d’exécution. Le verrou principal n'a pas pu être posé, car il semble qu'un autre processus
sur un autre serveur l'a déjà posé. Nous ne pouvons détecter les verrous
oubliés de serveur à serveur, donc vous devrez corriger cela manuellement.

Fichier verrou : $config.LOCK_FILE
Serveur verrouillant : $hostname

Fin d'exécution. Le verrou principal n'a pas pu être posé. Il semble qu'il y a un autre verrou
principal d'oublié. Essayez de relancer $program avec l'option --force. La liste {} comporte {} demandes de modération en attente. Notification de rejet non-interceptée Domaine non défini : $domain Nom de processus non-défini : $name Demande de désinscription Utilisateur : {}
 Bienvenue sur la liste de diffusion "$mlist.display_name"${digmode} Vous avez été désinscrits de la liste de diffusion $mlist.display_name Votre message à $mlist.fqdn_listname attend la validation d'un modérateur Votre nouvelle liste de diffusion : $fqdn_listname Vous avez été désinscrits de la liste de diffusion $mlist.display_name [Pas de détails disponibles sur la redirection] [Aucune raison n’est donnée] mauvais argument : $argument La liste de diffusion '$listname' vient d’être créée pour vous. Voici quelquesinformations basiques concernant cette liste.Il y a une interface par courriel pour les utilisateurs (pas lesadministrateurs) de votre liste. Vous pouvez obtenir des informations sur sonutilisation en envoyant un courriel avec seulement le mot 'help' dans l’objetou corps à l’adresse :    $request_emailVeuillez envoyer toutes vos questions à $site_email. Aide pour la liste de diffusion $listnameCeci est le courriel correspondant à la commande 'help' pour la version$version du gestionnaire de listes de diffusion GNU Mailman du domaine$domain. Vous trouverez ci-dessous les commandes que vous pouvez utiliser pourobtenir des informations et contrôler vos abonnements aux listes de diffusionMailman de ce site. Une commande peut être placée dans l’objet ou dans lecorps du message.Les commandes doivent être envoyées à l’adresse ${listname}-request@${domain}.Concernant les descriptions, les éléments entre "<>" sont requis et ceux entre"[]" sont optionnels. N’incluez pas les "<>" ou "[]" quand vous utilisez lescommandes.Les commandes suivantes sont valides :    $commandsLes questions et préoccupations à destination d’un être humain doivent êtreenvoyées à :    $administrator ipython n’est pas disponible, réglez use_ipython sur no En tant qu’administrateur d’une liste, votre autorisation est nécessaire pourvalider le message suivant :    Liste : $listname    De :    $sender_email    Objet : $subjectCe message a besoin d’une validation car :$reasonsVous pouvez vous rendre sur votre tableau de bord pour donner suite, ou non, àcette requête. Une demande d’inscription à une liste est en attente de votre validation :    Pour :  $member    Liste : $listname Une demande de désinscription à une liste est en attente de votre validation :    Pour :  $member    Liste : $listname $member a été inscrit(e) à $display_name avec succès. Le message de rejet attaché a été reçu, mais le format du rejet n’a pas étéreconnu ou aucune adresse de membre n’a pu être extraite de celui-ci. Cetteliste de diffusion a été configurée pour envoyer tous les messages de rejetinconnus aux administrateurs de la liste. $member a été retiré(e) de $display_name. Envoyez vos postes pour la liste de diffusion $display_name à	$listnamePour vous inscrire ou désinscrire par courriel, envoyez un message avec 'help'dans  l’objet ou le corps à	$request_emailVous pouvez contacter la personne gérant la liste en écrivant à	$owner_emailQuand vous répondez, veuillez éditer l’objet pour qu’il soit plus précis queRe: Contenu du résumé de $display_name ... _______________________________________________Liste de diffusion $display_name -- $listnamePour vous désinscrire, envoyez un courriel à ${short_listname}-leave@${domain} Confirmation de l’inscription de votre adresse électroniqueBonjour, c’est le serveur GNU Mailman de $domain.Nous avons reçu une demande d’inscription pour l’adresse électronique    $user_emailAvant de pouvoir utiliser GNU Mailman sur ce serveur, vous devez préalablementconfirmer que c’est bien votre adresse électronique. Vous pouvez le faire enrépondant à ce courriel sans toucher à son objet.Si vous ne souhaitez pas inscrire cette adresse électronique, vous pouvezsimplement ignorer ce message. Si vous pensez que vous avez été malicieusementinscrit à la liste, ou si vous avez n’importe quelle autre question, vouspouvez contacter    $owner_email Confirmation de la désinscription de votre adresse électroniqueBonjour, c’est le serveur GNU Mailman de $domain.Nous avons reçu une demande de désinscription pour l’adresse électronique    $user_emailPour que GNU Mailman puisse vous désinscrire, vous devez confirmer votrerequête. Vous pouvez le faire en répondant à ce courriel sans toucher à sonobjet.Si vous ne souhaitez pas désinscrire cette adresse électronique, vous pouvezsimplement ignorer ce message. Si vous pensez que quelqu’un a essayé de vousdésinscrire malicieusement de la liste, ou si vous avez n’importe quelle autrequestion, vous pouvez contacter    $owner_email Votre courriel à destination de '$listname' avec l’objet    $subjectest en attente de validation par un modérateur.Ce message a besoin d’une validation car :$reasonsSoit ce message sera posté sur la liste, soit vous recevrez unenotification avec la décision du modérateur. Nous avons reçu un message de votre adresse <$sender_email> demandant uneréponse automatique de la part de la liste de diffusion $listname.Le nombre de messages que nous avons reçus aujourd’hui : $count. Pour éviterdes problèmes tels que des boucles de courriels entre des robots, nousne vous enverrons pas de réponses supplémentaires aujourd’hui. Veuillezréessayer demain.Si vous pensez que ce message est une erreur, ou si vous avez des questions,veuillez contacter le propriétaire de la liste à l’adresse $owner_email. Votre message avec l’objet    $subjecta été reçu avec succès par la liste de diffusion $display_name. C’est un message de sonde. Vous pouvez l’ignorer.La liste de diffusion $listname a reçu un nombre important de messages derebond de votre part, ce qui peut indiquer qu’il y a un problème pour envoyerdes courriels à $sender_email. Un exemple est joint ci-dessous.Veuillez examiner ce message pour vous assurer qu’il n’y a pas de problèmeavec votre adresse électronique. Vous pouvez vérifier cela avecl’administrateur de vos courriels pour plus d’aide.Vous n’avez rien besoin de faire pour rester membre de la liste de diffusion.Si vous avez des questions ou rencontrez des problèmes, vous pouvez contacterle propriétaire de la liste de diffusion à l’adresse    $owner_email Votre requête à la liste de diffusion $listname    $requesta été rejetée par le modérateur de la liste. Le modérateur a donné la raisonsuivante :$reasonToute question ou commentaire doit être envoyé à l’administrateur de la listeà l’adresse suivante :    $owner_email Votre message à destination de la liste de diffusion $listname a été rejetépour les raisons suivantes :$reasonsLe message original reçu par Mailman est joint. Bienvenue dans la liste de diffusion "$display_name" !Pour écrire à cette liste, envoyez vos courriels à :    $listnameVous pouvez vous désinscrire ou ajuster vos paramètres par courriel en écrivantun message à :    $request_emailavec le mot 'help' dans l’objet ou le corps (n’incluez pas les guillemets).Vous recevrez en retour un message avec des instructions à suivre. Vous aurezbesoin de votre mot de passe pour changer vos paramètres, mais pour desraisons de sécurité, celui-ci n’est pas joint au présent message. Si vousavez oublié votre mot de passe, vous devrez le réinitialiser en passant parl’interface web. n/d 