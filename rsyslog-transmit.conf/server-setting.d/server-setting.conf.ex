###保存接受日志的位置及文件名
$templateRemote  "/data/log/%fromhost-ip%/%fromhost-ip%_%$YEAR%-%$MONTH%-%$DAY%.log"

###允许对应网段的客户端转发日志
$AllowedSender  192.168.30.0/24

###进行通信的ip以及端口
$ReceivedServer localhost/24

###支持的协议（TCP/UDP）
$TransmitProtocol  TCP/UDP
