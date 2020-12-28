��    j      l  �   �      	  a  	  �   s  �   G  }     �   �  '   m  �   �  �   A  Y   �  o   O  _   �  q    �  �  �  t  �   V    �  �     �   �  :   �  P   �  9   P  �   �  {   [   R   �   �   *!  �  "  I   �$     %  K   %  6   ]%  .   �%  -   �%  /   �%  <   !&     ^&     t&  K   �&     �&  %   �&  <   '  (   B'  5   k'  &   �'  3   �'  x   �'     u(     �(     �(  !   �(  #   �(  m  )     *  (   �*     �*     �*  :   �*  )   &+  (   P+  '   y+     �+     �+  M   �+  =   ,  O   B,     �,     �,     �,     �,     �,  #   �,  )   "-      L-  +   m-  0   �-  ,   �-     �-  0   .     F.     e.     �.  %   �.  8   �.     �.  .   /      D/  1   e/  -   �/  "   �/  "   �/     0  e   *0    �0  �   �1     /2     L2     i2  ;   �2  J   �2  D   3  P   L3  Q   �3  >   �3  J   .4  !   y4     �4  �  �4  �  M6  �   J9  �   9:  �   ;  �   �;  #   �<  �   �<  �   Q=  j   	>  �   t>  r   ?  �  v?    A    'C  �   9E  ^  �E  P  DK    �N  B   �O  V   �O  ;   5P    qP  �   �Q  I   R    UR  >  cS  P   �V     �V  W   W  W   YW  /   �W  &   �W  1   X  U   :X  #   �X  
   �X  w   �X     7Y  %   MY  D   sY  <   �Y  H   �Y  #   >Z  D   bZ  �   �Z     1[     P[  ,   p[  2   �[  '   �[  s  �[     l]  *   �]     �]     �]  E   �]  >   ,^  &   k^  *   �^     �^     �^  S   �^  R   %_  ^   x_  $   �_  $   �_     !`     >`     ^`  ,   m`  3   �`  %   �`  *   �`  6   a  5   Va  2   �a  0   �a  6   �a  #   'b     Kb  .   gb  T   �b      �b  6   c  0   Cc  E   tc  5   �c  +   �c  '   d     Dd  ]   _d  ,  �d  �   �e  "   zf  (   �f     �f  =   �f  F    g  =   gg  P   �g  R   �g  E   Ih  R   �h     �h     i        ]       .   4       %   C   ;   P   L       2   ,   \              6   K   +                  3                     @   c   (             7      	   
   e   <   F              h   &      `   b   B              *   S       V   #   W   H      d                 :   N      =   >                      f                    a   R                  -   j      "                  $   '   )   D   9          i   O   1   Z              E   !           ?   U   /   I   8           0          T   ^   5   Y       J      X       G   A   Q   M       [                 g   _    
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
         Add all member addresses in FILENAME with delivery mode as specified
    with -d/--delivery.  FILENAME can be '-' to indicate standard input.
    Blank lines and lines that start with a '#' are ignored.
         Configuration file to use.  If not given, the environment variable
    MAILMAN_CONFIG_FILE is consulted and used if set.  If neither are given, a
    default configuration file is loaded.     Delete all the members of the list.  If specified, none of -f/--file,
    -m/--member or --fromall may be specified.
         Delete list members whose addresses are in FILENAME in addition to those
    specified with -m/--member if any.  FILENAME can be '-' to indicate
    standard input.  Blank lines and lines that start with a '#' are ignored.
         Delete members from a mailing list.     Delete the list member whose address is ADDRESS in addition to those
    specified with -f/--file if any.  This option may be repeated for
    multiple addresses.
         Delete the member(s) specified by -m/--member and/or -f/--file from all
    lists in the installation.  This may not be specified together with
    -a/--all or -l/--list.
         Don't print status messages.  Error messages are still printed to standard
    error.     Don't restart the runners when they exit because of an error or a SIGUSR1.
    Use this only for debugging.     File to send the output to.  If not given, or if '-' is given, standard
    output is used.     Generate the MTA alias files upon startup. Some MTA, like postfix, can't
    deliver email if alias files mentioned in its configuration are not
    present. In some situations, this could lead to a deadlock at the first
    start of mailman3 server. Setting this option to true will make this
    script create the files and thus allow the MTA to operate smoothly.     If the master watcher finds an existing master lock, it will normally exit
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
    master lock.     Key to use for the lookup.  If no section is given, all the key-values pair
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
    archives through the web.  Tough luck!     Override the default set of runners that the master will invoke, which is
    typically defined in the configuration file.  Multiple -r options may be
    given.  The values for -r are passed straight through to bin/runner.     Override the list's setting for admin_notify_mchanges.     Override the list's setting for send_goodbye_message to
    deleted members.     Override the list's setting for send_welcome_message.     Run the named runner exactly once through its main loop.  Otherwise, the
    runner runs indefinitely until the process receives a signal.  This is not
    compatible with runners that cannot be run once.     Section to use for the lookup.  If no key is given, all the key-value pairs
    of the given section will be displayed.     Send the added members an invitation rather than immediately adding them.
         Set the added members delivery mode to 'regular', 'mime', 'plain',
    'summary' or 'disabled'.  I.e., one of regular, three modes of digest
    or no delivery.  If not given, the default is regular.  Ignored for invited
    members.     Start a runner.

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
         The list to operate on.  Required unless --fromall is specified.
      (Digest mode) $member unsubscribed from ${mlist.display_name} mailing list due to bounces $member's subscription disabled on $mlist.display_name $mlist.display_name mailing list probe message $mlist.display_name subscription notification $mlist.display_name unsubscription notification $mlist.fqdn_listname post from $msg.sender requires approval $name runs $classname (no subject) A previous run of GNU Mailman did not exit cleanly ({}).  Try using --force Accept a message. Already subscribed (skipping): $email An alternative directory to output the various MTA files to. Cannot import runner module: $class_path Cannot parse as valid email address (skipping): $line Discard a message and stop processing. Display more debugging information to the log file. For unknown reasons, the master lock could not be acquired.

Lock file: $config.LOCK_FILE
Lock host: $hostname

Exiting. Forward of moderated message GNU Mailman is already running Generating MTA alias maps Header "{}" matched a header rule Hold a message and stop processing. If you reply to this message, keeping the Subject: header intact, Mailman will
discard the held message.  Do this if the message is spam.  If you reply to
this message and include an Approved: header with the list password in it, the
message will be approved for posting to the list.  The Approved: header can
also appear in the first line of the body of the reply. Is the master even running? Last autoresponse notification for today Less verbosity List all mailing lists. List only those mailing lists that are publicly advertised List the available runner names and exit. Member not subscribed (skipping): $email Membership is banned (skipping): $email Moderation chain N/A New subscription request to $self.mlist.display_name from $self.address.email New unsubscription request from $mlist.display_name by $email New unsubscription request to $self.mlist.display_name from $self.address.email No child with pid: $pid No runner name given. No such list: $_list No such list: $listspec Original Message PID unreadable in: $config.PID_FILE Posting of your message titled "$subject" Print the Mailman configuration. Process DMARC reject or discard mitigations Regenerate the aliases appropriate for your MTA. Reject/bounce a message and stop processing. Reopening the Mailman runners Request to mailing list "$display_name" rejected Restarting the Mailman runners Show also the list descriptions Show also the list names Shutting down Mailman's master runner Signal the Mailman processes to re-open their log files. Stale pid file removed. Start the Mailman master and runner processes. Starting Mailman's master runner Stop and restart the Mailman runner subprocesses. Stop the Mailman master and runner processes. The built-in -owner posting chain. The built-in header matching chain The built-in moderation chain. The master lock could not be acquired because it appears as though another
master is already running. The master lock could not be acquired, because it appears as if some process
on some other host may have acquired it.  We can't test for stale locks across
host boundaries, so you'll have to clean this up manually.

Lock file: $config.LOCK_FILE
Lock host: $hostname

Exiting. The master lock could not be acquired.  It appears as though there is a stale
master lock.  Try re-running $program with the --force flag. Uncaught bounce notification Undefined runner name: $name Unsubscription request Welcome to the "$mlist.display_name" mailing list${digmode} You have been invited to join the $event.mlist.fqdn_listname mailing list. You have been unsubscribed from the $mlist.display_name mailing list Your confirmation is needed to join the $event.mlist.fqdn_listname mailing list. Your confirmation is needed to leave the $event.mlist.fqdn_listname mailing list. Your message to $mlist.fqdn_listname awaits moderator approval Your subscription for ${mlist.display_name} mailing list has been disabled [No bounce details are available] [No reason given] Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2020-10-25 22:24+0000
Last-Translator: Oğuz Ersen <oguzersen@protonmail.com>
Language-Team: Turkish <https://hosted.weblate.org/projects/gnu-mailman/mailman/tr/>
Language: tr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n != 1;
X-Generator: Weblate 4.3.2-dev
 
    -l seçeneğinin döndürdüğü dizgelerden biri olması gereken adı belirtilen
    çalıştırıcıyı başlat.

    Bir kuyruk dizinini yöneten çalıştırıcılar için, bu kuyruğa birden fazla çalıştırıcı
    işlemi atamak için belirtilmişse isteğe bağlı `dilim:aralık` değeri kullanılır.
    aralık, kuyruk için toplam çalıştırıcı sayısı iken dilim, 0 ile aralık arasında bu
    çalıştırıcının numarasıdır.  Bir kuyruk yönetmeyen çalıştırıcılar için, dilim ve
    aralık dikkate alınmaz.

    `dilim:aralık` biçimini kullanırken, kuyruk için her çalıştırıcıya aynı aralık
    değerinin verildiğinden emin olmalısınız.  `dilim:aralık` belirtilmezse,
    1:1 değeri kullanılır.
         FILENAME içindeki tüm üye adreslerini -d/--delivery seçeneğiyle belirtilen
    teslimat modu ile ekle.  FILENAME standart girişi belirtmek için '-' olabilir.
    Boş satırlar ve '#' ile başlayan satırlar yok sayılır.
         Kullanılacak yapılandırma dosyası. Belirtilmezse,
    MAILMAN_CONFIG_FILE ortam değişkenine başvurulur ve ayarlanmışsa kullanılır.
    Hiçbiri belirtilmemişse öntanımlı bir yapılandırma dosyası yüklenir.     Listenin tüm üyelerini sil.  Bu belirtilirse, -f/--file, -m/--member
    veya --fromall seçeneklerinden hiçbiri belirtilemez.
         Varsa -m/--member ile belirtilenlere ek olarak adresleri FILENAME içinde
    olan liste üyelerini sil.  FILENAME standart girişi belirtmek için '-' olabilir.
    Boş satırlar ve '#' ile başlayan satırlar yok sayılır.
         Üyeleri posta listesinden sil.     Varsa -f/--file ile belirtilenlere ek olarak adresi ADDRESS olan liste üyesini sil.
    Bu seçenek birden çok adres için tekrar edilebilir.
         -m/--member ve/veya -f/--file ile belirtilen üye(ler)i kurulumdaki tüm
    listelerden sil.  Bu seçenek, -a/--all veya -l/--list seçenekleriyle birlikte
    belirtilemez.
         Durum mesajlarını yazdırma.  Hata mesajları yine de standart hata çıkışına
    yazdırılır.     Çalıştırıcılar bir hata veya SIGUSR1 nedeniyle çıktığında yeniden başlatma.
    Bunu yalnızca hata ayıklama için kullanın.     Çıktının gönderileceği dosya.  Belirtilmezse veya '-' belirtilirse,
    standart çıkış kullanılır.     Başlangıçta MTA takma ad dosyalarını oluştur. Postfix gibi bazı MTA'lar,
    yapılandırmasında belirtilen takma ad dosyaları yoksa e-posta gönderemez.
    Bu, bazı durumlarda mailman3 sunucusunun ilk başlangıçta kilitlenmesine
    neden olabilir. Bu seçeneğin doğru olarak ayarlanması, bu betiğin dosyaları
    oluşturmasını ve dolayısıyla MTA'nın sorunsuz çalışmasını sağlar.     Ana izleyici mevcut bir ana kilit bulması durumunda, normalde bir hata
    mesajı ile çıkacaktır.  Bu seçenekle birlikte, ana işlem ek bir denetim
    gerçekleştirecektir.  Kilit dosyasında belirtilen ana makine/PID ile eşleşen
    bir işlem çalışıyorsa, ana işlem yine de kilidi elle temizlemenizi gerektirecek
    şekilde çıkacaktır.  Ancak eşleşen bir işlem bulunmazsa, ana işlem eski olarak
    görünen kilidi kaldıracak ve ana kilidi elde etmek için başka bir girişimde
    bulunacaktır.     Ana izleyici mevcut bir ana kilit bulması durumunda, normalde bir hata
    mesajı ile çıkacaktır.  Bu seçenekle birlikte, ana işlem ek bir denetim
    gerçekleştirecektir.  Kilit dosyasında belirtilen ana makine/PID ile eşleşen
    bir işlem çalışıyorsa, ana işlem yine de kilidi elle temizlemenizi gerektirecek
    şekilde çıkacaktır.  Ancak eşleşen bir işlem bulunmazsa, ana işlem eski olarak
    görünen kilidi kaldıracak ve ana kilidi elde etmek için başka bir girişimde
    bulunacaktır.     Arama için kullanılacak anahtar.  Bölüm belirtilmezse, belirtilen anahtarla
    eşleşen herhangi bir bölümdeki tüm anahtar/değer çiftleri görüntülenecek.     Ana alt işlem izleyicisi.

    Yapılandırılmış çalıştırıcıları başlatın ve izleyin, çalışıyor durumda kaldıklarından
    emin olun.  Her çalıştırıcı sırayla çatallanır ve çalıştırılır (exec), ana işlem onları
    işlem kimlikleriyle bekler.  Bir alt çalıştırıcının çıktığını algıladığında, onu yeniden
    başlatabilir.

    Çalıştırıcılar SIGINT, SIGTERM, SIGUSR1 ve SIGHUP sinyallerine yanıt verir.  SIGINT,
    SIGTERM ve SIGUSR1 sinyalleri bir çalıştırıcının temiz bir şekilde çıkmasına neden
    olur.  Ana işlem, SIGUSR1 veya başka bir çıkış koşulu nedeniyle (örneğin
    yakalanmamış bir istisna) çıkan çalıştırıcıları yeniden başlatacaktır.  SIGHUP sinyali
    ana işlemin ve çalıştırıcıların günlük dosyalarını kapatmalarına ve bir sonraki
    yazdırılan mesajda yeniden açmalarına neden olur.

    Ana işlem ayrıca SIGINT, SIGTERM, SIGUSR1 ve SIGHUP sinyallerine yanıt verir ve
    bunları basitçe çalıştırıcılara iletir.  SIGHUP sinyali alındığında ana işlemin kendi
    günlük dosyalarını kapatacağını ve yeniden açacağını unutmayın.  Ana işlem ayrıca
    yapılandırma dosyasında belirtilen dosyaya kendi işlem kimliğini kaydeder, ancak
    normalde bu işlem kimliğini (PID) doğrudan kullanmanız gerekmez.     Normalde bu betik, kullanıcı ve grup kimliği 'mailman' kullanıcı ve grubuna
    ayarlanmadıysa (Mailman'i yapılandırdığınızda tanımlandığı gibi) çalışmayı
    reddedecektir.  Bu betik root olarak çalıştırılırsa, denetim yapılmadan önce
    bu kullanıcı ve gruba geçiş yapacaktır.

    Bu, test etme ve hata ayıklama amaçları için uygun olmayabilir, bu nedenle -u
    seçeneği, UID/GID'yi ayarlayan ve denetleyen adımın atlandığı ve programın
    geçerli kullanıcı ve grup olarak çalıştırıldığı anlamına gelir.  Bu seçenek, normal
    çalışma ortamları için tavsiye edilmez.

    Yine de -u ile çalıştırırsanız ve mailman grubunda değilseniz, web üzerinden bir
    listenin arşivlerini silememek gibi izin sorunlarınız olabileceğini unutmayın.
    Şansınıza küsün!     Genellikle yapılandırma dosyasında tanımlanan, ana işlemin başlatacağı
    öntanımlı çalıştırıcı kümesini geçersiz kıl.  Birden çok -r seçeneği belirtilebilir.
    -r için belirtilen değerler doğrudan bin/runner işlemine iletilir.     admin_notify_mchanges için listenin ayarını geçersiz kıl.     Listenin, silinen üyeler için send_goodbye_message ayarını
    geçersiz kıl.     Listenin send_welcome_message ayarını geçersiz kıl.     Adı belirtilen çalıştırıcıyı ana döngüsü boyunca tam olarak bir kez çalıştır.
    Aksi takdirde işlem bir sinyal alana kadar çalıştırıcı süresiz olarak çalışır.
    Bu, bir defa çalıştırılamayan çalıştırıcılarla uyumlu değildir.     Arama için kullanılacak bölüm.  Anahtar belirtilmezse, belirtilen
    bölümün tüm anahtar/değer çiftleri görüntülenecek.     Eklenen üyelere onları hemen eklemek yerine bir davet gönder.
         Eklenen üyelerin teslimat modunu 'regular', 'mime', 'plain', 'summary'
    veya 'disabled' olarak ayarla.  Yani, bir tane normal, üç tane özet modu
    veya teslimat yok. Belirtilmezse, öntanımlı olan normaldir.  Davet edilen
    üyeler için yok sayılır.     Bir çalıştırıcı başlat.

    Komut satırında adı geçen çalıştırıcı başlatılır ve ana döngüsü boyunca
    bir kez (bunu destekleyen çalıştırıcılar için) veya sürekli olarak çalıştırabilir.
    Ana çalıştırıcı tüm alt işlemlerini ikinci şekilde başlatır.

    -l veya -h seçenekleri verilmedikçe -r seçeneği gereklidir ve argümanı -l
    seçeneği tarafından görüntülenen isimlerden biri olmalıdır.

    Normalde bu betik `mailman start` içinden başlatılmalıdır.  Ayrı ayrı veya
    -o seçeneği ile çalıştırmak genellikle yalnızca hata ayıklama için faydalıdır.
    Bu şekilde çalıştırıldığında, bazı hata işleme davranışlarını ince bir şekilde
    değiştiren $MAILMAN_UNDER_MASTER_CONTROL ortam değişkeni
    ayarlanacaktır.
         Üzerinde işlem yapılacak liste.  --fromall belirtilmezse gereklidir.
      (Özet modu) $member, geri dönmeler nedeniyle ${mlist.display_name} posta listesinden çıkarıldı $member üyesinin $mlist.display_name üzerindeki aboneliği devre dışı bırakıldı $mlist.display_name posta listesi sorgu mesajı $mlist.display_name abonelik bildirimi $mlist.display_name abonelikten çıkma bildirimi $msg.sender kişisinin $mlist.fqdn_listname listesine gönderisi için onay gerekiyor $name, $classname çalıştırıyor (konu yok) Önceki bir GNU Mailman çalıştırması temiz bir şekilde çıkmadı ({}).  --force seçeneğini kullanmayı deneyin Bir mesajı kabul et. Zaten abone oldu (atlanıyor): $email Çeşitli MTA dosyalarının çıktısı için alternatif bir dizin. Çalıştırıcı modülü içe aktarılamıyor: $class_path Geçerli e-posta adresi olarak ayrıştırılamıyor (atlanıyor): $line Bir mesajı at ve işlemeyi durdur. Günlük dosyasında daha fazla hata ayıklama bilgisi görüntüle. Bilinmeyen nedenlerden dolayı ana kilit elde edilemedi.

Kilit dosyası: $config.LOCK_FILE
Kilit ana makinesi: $hostname

Çıkılıyor. Denetlenen mesajın iletilmesi GNU Mailman zaten çalışıyor MTA takma ad eşleştirmeleri oluşturuluyor "{}" başlığı bir başlık kuralıyla eşleşti Bir mesajı beklet ve işlemeyi durdur. Bu mesajı Konu: başlığını olduğu gibi bırakarak yanıtlarsanız, Mailman
bekletilen mesajı atacaktır.  Mesaj spam ise bunu yapın.  Bu mesajı yanıtlarsanız
ve içinde liste parolasının olduğu bir Onaylandı: başlığı eklerseniz, mesajın
listeye gönderilmesi onaylanacaktır.  Onaylandı: başlığı, yanıt metninin ilk
satırında da görünebilir. Ana işlem çalışıyor mu? Bugün için son otomatik yanıt bildirimi Daha az ayrıntı Tüm posta listelerini listele. Yalnızca herkese açık olarak tanıtılan posta listelerini listele Kullanılabilir çalıştırıcı adlarını listele ve çık. Üye abone değil (atlanıyor): $email Üyelik yasaklanmış (atlanıyor): $email Denetim zinciri Yok $self.address.email adresinden $self.mlist.display_name için yeni abonelik isteği $email tarafından yeni $mlist.display_name listesi aboneliğinden çıkma isteği $self.address.email adresinden $self.mlist.display_name için yeni abonelikten çıkma isteği $pid kimliğine sahip alt işlem yok Çalıştırıcı adı belirtilmedi. Böyle bir liste yok: $_list Böyle bir liste yok: $listspec Orijinal Mesaj $config.PID_FILE dosyasında PID okunamıyor "$subject" başlıklı mesajınızın gönderilmesi Mailman yapılandırmasını yazdır. DMARC reddet veya at azaltmalarını işle MTA'nız için uygun takma adları yeniden oluşturun. Bir mesajı reddet/geri döndür ve işlemeyi durdur. Mailman çalıştırıcıları yeniden açılıyor "$display_name" posta listesine istek reddedildi Mailman çalıştırıcıları yeniden başlatılıyor Liste açıklamalarını da göster Liste adlarını da göster Mailman ana çalıştırıcısı kapatılıyor Mailman işlemlerine günlük dosyalarını yeniden açmaları için sinyal gönder. Eski PID dosyası kaldırıldı. Mailman ana ve çalıştırıcı işlemlerini başlat. Mailman ana çalıştırıcısı başlatılıyor Mailman çalıştırıcı alt işlemlerini durdur ve yeniden başlat. Mailman ana ve çalıştırıcı işlemlerini durdur. Yerleşik -owner (sahip) gönderme zinciri. Yerleşik başlık eşleştirme zinciri Yerleşik denetim zinciri. Başka bir ana işlem zaten çalışıyor gibi göründüğü için ana kilit elde
edilemedi. Başka bir ana makinedeki başka bir işlem onu almış gibi göründüğü için ana kilit
elde edilemedi.  Farklı ana makineler üzerindeki eski kilitleri test edemiyoruz, bu
nedenle bunu elle temizlemeniz gerekecek.

Kilit dosyası: $config.LOCK_FILE
Kilit ana makinesi: $hostname

Çıkılıyor. Ana kilit elde edilemedi.  Eski bir ana kilit varmış gibi görünüyor.  $program'ı
--force seçeneğiyle yeniden çalıştırmayı deneyin. Yakalanmayan geri dönme bildirimi Tanımsız çalıştırıcı adı: $name Abonelikten çıkma isteği "$mlist.display_name" posta listesine hoş geldiniz${digmode} $event.mlist.fqdn_listname posta listesine katılmaya davet edildiniz. $mlist.display_name posta listesi aboneliğinden çıktınız $event.mlist.fqdn_listname posta listesine katılmak için onayınız gerekiyor. $event.mlist.fqdn_listname posta listesinden ayrılmak için onayınız gerekiyor. $mlist.fqdn_listname listesine mesajınız moderatör onayı bekliyor ${mlist.display_name} posta listesi için aboneliğiniz devre dışı bırakıldı [Geri dönme ayrıntısı yok] [Neden belirtilmedi] 