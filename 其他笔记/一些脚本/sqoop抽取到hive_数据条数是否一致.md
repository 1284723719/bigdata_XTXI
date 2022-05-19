~~~shell
#2-统计mysql表dd_table的条数
mysql_log=`sqoop eval \
--connect jdbc:mysql://hadoop01:3306/nev \
--username root \
--password 123456 \
--query "select count(*) from web_chat_text_ems_2019_07"`
# | 管道，将左边的结果输出 给到 右边作为输入，  awk -F表示按什么来切分，'{print $4}'表示返回切完后的第4个值
mysql_cnt=`echo $mysql_log | awk -F '|' '{print $4}' | awk -F ' ' '{print $1}'`


#3-统计hive表dd_table的条数
hive_log=`hive -e 'select count(*) from itcast_ods.web_chat_text_ems'`
#hive_cnt=`echo $hive_log | awk -F ' ' '{print $2}'`
#4-比较2边的条数是否一致。
if [ $mysql_cnt -eq $hive_log ] ; then
  echo "mysql表的条数是$mysql_cnt,hive表的条数是$hive_cnt，2边一致"
else
  echo "mysql表的条数是$mysql_cnt,hive表的条数是$hive_cnt，2边不一致"
fi
~~~

