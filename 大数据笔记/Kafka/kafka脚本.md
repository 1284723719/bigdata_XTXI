~~~shell
#!/bin/bash
#kafka脚本
if [ $# -lt 1 ]
then 
 echo "Usage: kf.sh {start|stop|kc [topic]|kp [topic] |list |delete [topic] |describe [topic]}"
 exit
fi
case $1 in 
start)
for i in node1 node2 node3
do
 echo "====================> START $i KF <===================="
 ssh $i /export/server/kafka/bin/kafka-server-start.sh -daemon /export/server/kafka/config/server.properties 
wait
done
;;
stop)
for i in node1 node2 node3
do
 echo "====================> STOP $i KF <===================="
 ssh $i /export/server/kafka/bin/kafka-server-stop.sh 
 wait
done
;;
kc)
if [ $2 ]
then
 kafka-console-consumer.sh --bootstrap-server node1:9092,node2:9092,node3:9092 --topic $2
else
 echo "Usage: kf.sh {start|stop|kc [topic]|kp [topic] |list |delete [topic] |describe [topic]}"
fi
;;
kp)
if [ $2 ]
then 
 kafka-console-producer.sh --broker-list node1:9092,node2:9092,node3:9092 --topic $2
else
 echo "Usage: kf.sh {start|stop|kc [topic]|kp [topic] |list |delete [topic] |describe [topic]}"
fi
;;
list)
kafka-topics.sh --list --bootstrap-server node1:9092,node2:9092,node3:9092
;;
describe)
if [ $2 ]
then
kafka-topics.sh --describe --bootstrap-server node1:9092,node2:9092,node3:9092 --topic $2
else
echo "Usage: kf.sh {start|stop|kc [topic]|kp [topic] |list |delete [topic] |describe [topic]}"
fi 
;;
delete)
if [ $2 ]
then
kafka-topics.sh --delete --bootstrap-server node1:9092,node2:9092,node3:9092 --topic $2
else
echo "Usage: kf.sh {start|stop|kc [topic]|kp [topic] |list |delete [topic] |describe [topic]}"
fi
;;
*)
 echo "Usage: kf.sh {start|stop|kc [topic]|kp [topic] |list |delete [topic] |describe [topic]}"
 exit
;;
esac
~~~

