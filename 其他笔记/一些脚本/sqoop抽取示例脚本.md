~~~~shell
#示例抽取到HDFS上
sqoop import \
--connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
--username ciss \
--password 123456 \
--table CISS4.CISS_SERVICE_WORKORDER \
--delete-target-dir \
--target-dir /test/full_imp/ciss4.ciss_service_workorder \
--null-string "\\N" \
--null-non-string "\\N" \
--fields-terminated-by "\001" \
-m 1
#-------------------------------------分隔符------------------------------------
#抽取到HDFS上为Avro格式 添加 --as-avrodatafile  
#Avro介绍移步到大数据文件下Hive文件
#用arvo这种格式会生成一个Java和avsc文件（表的schema信息）文件下面是指定文件存在哪里 是sqoop命令
#--outdir logs/java_code
#注意：如果使用了MR的Uber模式，必须在程序中加上以下参数避免类冲突问题
sqoop import \
-Dmapreduce.job.user.classpath.first=true \
--connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
--username ciss \
--password 123456 \
--table CISS4.CISS_SERVICE_WORKORDER \
--delete-target-dir \
--target-dir /test/full_imp/ciss4.ciss_service_workorder \
--as-avrodatafile \
--fields-terminated-by "\001" \
--null-string "\\N" \
--null-non-string "\\N" \
--outdir logs/java_code \
-m 1

#示例封装arvo格式脚本
#!/bin/bash
#export path
source /etc/profile
#export the tbname files
TB_NAME=/opt/datas/shell/test_full_table.txt
#export the import opt
IMP_OPT="sqoop import -Dmapreduce.job.user.classpath.first=true"
#export the jdbc opt
JDBC_OPT="--connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin --username ciss --password 123456"

#read tbname and exec sqoop解释:done < 文件名，会读取每行数据循环一次
while read tbname
do
  ${IMP_OPT} ${JDBC_OPT} --table ${tbname^^} --delete-target-dir --target-dir /test/full_imp/${tbname^^} --as-avrodatafile --fields-terminated-by "\001" -m 1
done < ${TB_NAME}


#Schema备份及上传（说明）用arvo这种格式会生成一个Java和avsc文件（表的schema信息）文件下面是指定文件存在哪里 是sqoop命令
#--outdir logs/java_code   （本地路径）

**Avro文件本地存储**
workhome=/opt/sqoop/one_make
--outdir ${workhome}/java_code

**Avro文件HDFS存储**
hdfs_schema_dir=/data/dw/ods/one_make/avsc
hdfs dfs -put ${workhome}/java_code/*.avsc ${hdfs_schema_dir}

- **Avro文件本地打包**
local_schema_backup_filename=schema_${biz_date}.tar.gz
tar -czf ${local_schema_backup_filename} ./java_code/*.avsc

**Avro文件HDFS备份**
hdfs_schema_backup_filename=${hdfs_schema_dir}/avro_schema_${biz_date}.tar.gz
hdfs dfs -put ${local_schema_backup_filename} ${hdfs_schema_backup_filename}

- 运行测试
cd /opt/sqoop/one_make/
./upload_avro_schema.sh 

验证结果
/data/dw/ods/one_make/avsc/
*.avsc
schema_20210101.tar.gz

#-------------------------------------分隔符------------------------------------

#sqoop增量方式
#Append
#要求：必须有一列自增的值，按照自增的int值进行判断
#特点：只能导入增加的数据，无法导入更新的数据
#场景：数据只会发生新增，不会发生更新的场景
sqoop import \
--connect jdbc:mysql://node3:3306/sqoopTest \
--username root \
--password 123456 \
--table tb_tohdfs \
--target-dir /sqoop/import/test02 \
--fields-terminated-by '\t' \
--check-column id \
--incremental append \
--last-value 0 \
--null-string "\\N" \
--null-non-string "\\N" \
-m 1

#Lastmodified
#要求：必须包含动态时间变化这一列，按照数据变化的时间进行判断
#特点：既导入新增的数据也导入更新的数据
#场景：一般无法满足要求，所以不用
sqoop import \
--connect jdbc:mysql://node3:3306/sqoopTest \
--username root \
--password 123456 \
--table tb_lastmode \
--target-dir /sqoop/import/test03 \
--fields-terminated-by '\t' \
--incremental lastmodified \
--check-column lastmode \
--last-value '2021-06-06 16:09:32' \
--null-string "\\N" \
--null-non-string "\\N" \
-m 1

#特殊方式：select语句过滤日期
#要求：每次运行的输出目录不能相同
#特点：自己实现增量的数据过滤，可以实现新增和更新数据的采集
#场景：一般用于自定义增量采集每天的分区数据到Hive
sqoop  import \
--connect jdbc:mysql://node3:3306/db_order \
--username root \
--password-file file:///export/data/sqoop.passwd \
--query "select * from tb_order where substring(create_time,1,10) = '2021-09-14' or substring(update_time,1,10) = '2021-09-14' and \$CONDITIONS " \
--delete-target-dir \
--target-dir /nginx/logs/tb_order/daystr=2021-09-14 \
--fields-terminated-by '\t' \
--null-string "\\N" \
--null-non-string "\\N" \
-m 1

~~~~

