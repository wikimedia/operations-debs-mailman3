��            )   �      �  �   �     a  K   p  6   �  .   �  -   "  /   P     �  x   �       M   #  =   q  O   �     �  )     0   :  e   k    �  �   �     p     �  ;   �  J   �  D   +	  P   p	  Q   �	  J   
  !   ^
     �
  �  �
  �   <     �  @   �  >   8  ,   w      �  &   �     �  �   �     �  M   �  :   �  V   !     x  *   �  2   �  @   �  �   $  t   !     �     �  :   �  @   �  0   8  @   i  @   �  ;   �     '     <                        
                                                            	                                                         Configuration file to use.  If not given, the environment variable
    MAILMAN_CONFIG_FILE is consulted and used if set.  If neither are given, a
    default configuration file is loaded.  (Digest mode) $member unsubscribed from ${mlist.display_name} mailing list due to bounces $member's subscription disabled on $mlist.display_name $mlist.display_name mailing list probe message $mlist.display_name subscription notification $mlist.display_name unsubscription notification (no subject) For unknown reasons, the master lock could not be acquired.

Lock file: $config.LOCK_FILE
Lock host: $hostname

Exiting. Forward of moderated message New subscription request to $self.mlist.display_name from $self.address.email New unsubscription request from $mlist.display_name by $email New unsubscription request to $self.mlist.display_name from $self.address.email Original Message Posting of your message titled "$subject" Request to mailing list "$display_name" rejected The master lock could not be acquired because it appears as though another
master is already running. The master lock could not be acquired, because it appears as if some process
on some other host may have acquired it.  We can't test for stale locks across
host boundaries, so you'll have to clean this up manually.

Lock file: $config.LOCK_FILE
Lock host: $hostname

Exiting. The master lock could not be acquired.  It appears as though there is a stale
master lock.  Try re-running $program with the --force flag. Uncaught bounce notification Unsubscription request Welcome to the "$mlist.display_name" mailing list${digmode} You have been invited to join the $event.mlist.fqdn_listname mailing list. You have been unsubscribed from the $mlist.display_name mailing list Your confirmation is needed to join the $event.mlist.fqdn_listname mailing list. Your confirmation is needed to leave the $event.mlist.fqdn_listname mailing list. Your subscription for ${mlist.display_name} mailing list has been disabled [No bounce details are available] [No reason given] Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2020-12-05 04:17+0000
Last-Translator: Cube Kassaki <2524737581@qq.com>
Language-Team: Chinese (Simplified) <https://hosted.weblate.org/projects/gnu-mailman/mailman/zh_Hans/>
Language: zh_Hans
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
X-Generator: Weblate 4.4-dev
     要使用的配置文件。如果没有给出，会查找是否设置了
    MAILMAN_CONFIG_FILE 环境变量。如果都没有，
    加载默认配置文件。  （摘要模式） 由于退回而导致 $member 成员退订 ${mlist.display_name} $member 成员的 $mlist.display_name 的订阅已经被关闭 $mlist.display_name 邮件列表检测消息 $mlist.display_name 订阅通知 $mlist.display_name 取消订阅通知 （没有主题） 由于某些未知原因，无法获取主锁。

锁定的文件：$config.LOCK_FILE
锁定的主机：$hostname

正在退出。 转发转发的邮件 新的来自 $self.address.email 对 $self.mlist.display_name 的订阅请求 新的退订请求来自 $email 通过 $mlist.display_name 新的来自 $self.address.email 对 $self.mlist.display_name 的取消订阅的请求 原始消息 以 "$subject" 为标题发布你的消息 对邮件列表 "$display_name" 的请求被拒绝 无法获取主机锁因为另外一个
主机已经在运行。 无法获取主锁，因为似乎其他主机上的某个进程可能已获取了主锁。
我们无法跨主机边界测试过时的锁，
因此您必须手动清理。

锁定的文件：$config.LOCK_FILE
锁定的主机：$hostname

正在退出。 无法获取主机锁。似乎有一个过时的主机锁。
可以尝试重新用 --force 选项运行 $program 。 未捕获的回报信息 退订请求 欢迎加入 "$mlist.display_name" 邮件列表 ${digmode} 你已被邀请加入 $event.mlist.fqdn_listname 邮件列表。 你已经退订 $mlist.display_name 邮件列表 你需要确认加入 $event.mlist.fqdn_listname 邮件列表。 你需要确认离开 $event.mlist.fqdn_listname 邮件列表。 你对 ${mlist.display_name} 邮件列表的订阅已关闭 [没有回复信息] [没有给出原因] 