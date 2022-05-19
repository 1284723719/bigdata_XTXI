# 编写脚本(python或shell)自动上传avsc文件到hdfs目录

## 定义上传文件功能变量

(1) workhome：项目的工作目录

​	 /opt/sqoop/one_make

(2) hdfs_schema_dir：avro文件存放目录

​	/data/dw/ods/onemake/avsc

(3) biz_date：压缩文件日期

​	20210101

(4) biz_fmt_date：日志日期

​	2021-01-01

(5) local_schema_backup_filename：本地备份文件名

​	schema_${biz_date}.tar.gz

(6) hdfs_schema_backup_filename：hdfs备份文件名

​	avro_schema_${biz_date}.tar.gz

(7) log_file：日志文件全路径名

​	workhome/log/upload_avro_schema_${biz_fmt_date}.log

## 定义日志打印方法

(1) cur_time：当前时间

(2) `${cur_time} $*`：执行日志，打印时间+日志打印方法后的字符串

(3) 追加日志到log文件中

## 加载环境变量文件，并进入项目的工作目录

## 检查hdfs存储的avro目录是否存在(以下检查avro目录)

(1) 打印日志

(2) hdfs dfs -test：测试目录是否存在

```shell
#  hadoop fs [generic options] [-test -[defsz] <path>]
# -test -[defsz] <path> :
#   Answer various questions about <path>, with result via exit status.
#     -d  return 0 if <path> is a directory.
#     -e  return 0 if <path> exists.
#     -f  return 0 if <path> is a file.
#     -s  return 0 if file <path> is greater than zero bytes in size.
#     -z  return 0 if file <path> is zero bytes in size, else return 1.
```

## 判断目录是否存在，不存在就创建avro目录

(1) 打印avro目录不存在的日志

(2) 打印创建avro目录的日志

(3) hdfs -dfs -mkdir：递归创建avro目录

## 检查hdfs上的avro目录下表的avro文件是否存在(hdfs上不存在就上传全部的avro文件)

(1) 打印日志上传全部的avro文件

(2) 打印日志执行上传文件命令

(3) hdfs -hdfs put：上传全部的以.avro结尾的文件(/fullpath/*.avro)

## 检查linux本地文件备份是否存在(本地不存在，则创建avro的压缩文件)

(1) 打印检查本地备份文件是否存在的日志

(2) ! -e ：判断本地备份文件是否存在，不存在就创建avro压缩文件

(3) 打印进入压缩文件逻辑日志

(4) 打印执行压缩文件命令日志

(5) tar -czf：执行压缩avsc文件命令

## 备份avro压缩文件上传到hdfs

(1) 打印检查hdfs上的avro备份压缩文件是否存在日志

(2) 执行检查hdfs上的avro备份压缩文件是否存在命令

(3) 打印上传备份文件到hdfs的日志

(4) 打印执行上传备份文件到hdfs的命令日志

(5) hdfs dfs -put：执行上传avro备份文件到hdfs命令

```shell
#!/usr/bin/env bash
# 上传
# /bin/bash
workhome=/opt/sqoop/one_make
hdfs_schema_dir=/data/dw/ods/one_make/avsc
biz_date=20210101
biz_fmt_date=2021-01-01
local_schema_backup_filename=schema_${biz_date}.tar.gz
hdfs_schema_backup_filename=${hdfs_schema_dir}/avro_schema_${biz_date}.tar.gz
log_file=${workhome}/log/upload_avro_schema_${biz_fmt_date}.log

# 打印日志
log() {
    cur_time=`date "+%F %T"`
    echo "${cur_time} $*" >> ${log_file}
}

source /etc/profile
cd ${workhome}

#  hadoop fs [generic options] [-test -[defsz] <path>]
# -test -[defsz] <path> :
#   Answer various questions about <path>, with result via exit status.
#     -d  return 0 if <path> is a directory.
#     -e  return 0 if <path> exists.
#     -f  return 0 if <path> is a file.
#     -s  return 0 if file <path> is greater than zero bytes in size.
#     -z  return 0 if file <path> is zero bytes in size, else return 1.

log "Check if the HDFS Avro schema directory ${hdfs_schema_dir}..."
hdfs dfs -test -e ${hdfs_schema_dir} > /dev/null

if [ $? != 0 ]; then
    log "Path: ${hdfs_schema_dir} is not exists. Create a new one."
    log "hdfs dfs -mkdir -p ${hdfs_schema_dir}"
    hdfs dfs -mkdir -p ${hdfs_schema_dir}
fi

log "Check if the file ${hdfs_schema_dir}/CISS4_CISS_BASE_AREAS.avsc has uploaded to the HFDS..."
hdfs dfs -test -e ${hdfs_schema_dir}/CISS4_CISS_BASE_AREAS.avsc > /dev/null
if [ $? != 0 ]; then
    log "Upload all the .avsc schema file."
    log "hdfs dfs -put ${workhome}/java_code/*.avsc ${hdfs_schema_dir}"
    hdfs dfs -put ${workhome}/java_code/*.avsc ${hdfs_schema_dir}
fi

# backup
log "Check if the backup tar.gz file has generated in the local server..." 
if [ ! -e ${local_schema_backup_filename} ]; then
    log "package and compress the schema files"
    log "tar -czf ${local_schema_backup_filename} ./java_code/*.avsc"
    tar -czf ${local_schema_backup_filename} ./java_code/*.avsc
fi

log "Check if the backup tar.gz file has upload to the HDFS..."
hdfs dfs -test -e ${hdfs_schema_backup_filename} > /dev/null
if [ $? != 0 ]; then
    log "upload the schema package file to HDFS"
    log "hdfs dfs -put ${local_schema_backup_filename} ${hdfs_schema_backup_filename}"
    hdfs dfs -put ${local_schema_backup_filename} ${hdfs_schema_backup_filename}
fi
```

------

```python
#!/usr/bin/env python
# @Time : 2021/7/20 15:46
# @desc :
__coding__ = "utf-8"
__author__ = "itcast"

# import pyhdfs
import logging
import os

workhome = '/opt/sqoop/one_make'
hdfs_schema_dir = '/data/dw/ods/one_make/avsc'
biz_date = '20210101'
biz_fmt_date = '2021-01-01'
local_schema_backup_filename = 'schema_%s.tar.gz' % biz_date
hdfs_schema_backup_filename = '%s/avro_schema_%s.tar.gz' % (hdfs_schema_dir, biz_date)
log_file = '%s/log/upload_avro_schema_%s.log' % (workhome, biz_fmt_date)

# append log to file
logging.basicConfig(level=logging.INFO,
                    filename=log_file,
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

os.system('source /etc/profile')
os.system('cd %s' % workhome)

#  hadoop fs [generic options] [-test -[defsz] <path>]
# -test -[defsz] <path> :
#   Answer various questions about <path>, with result via exit status.
#     -d  return 0 if <path> is a directory.
#     -e  return 0 if <path> exists.
#     -f  return 0 if <path> is a file.
#     -s  return 0 if file <path> is greater than zero bytes in size.
#     -z  return 0 if file <path> is zero bytes in size, else return 1.
logging.info('Check if the HDFS Avro schema directory %s...', hdfs_schema_dir)
# hdfs = pyhdfs.HdfsClient(hosts="node1,9000", user_name="hdfs")
# print(hdfs.listdir('/'))
# hdfs dfs -test -e ${hdfs_schema_dir} > /dev/null
commStatus = os.system('hdfs dfs -test -e %s > /dev/null' % hdfs_schema_dir)
if commStatus is not 0:
    logging.info('Path: %s is not exists. Create a new one.', hdfs_schema_dir)
    logging.info('hdfs dfs -mkdir -p %s', hdfs_schema_dir)
    os.system('hdfs dfs -mkdir -p %s' % hdfs_schema_dir)

logging.info('Check if the file %s/CISS4_CISS_BASE_AREAS.avsc has uploaded to the HFDS...', hdfs_schema_dir)
commStatus = os.system('hdfs dfs -test -e %s/CISS4_CISS_BASE_AREAS.avsc > /dev/null' % hdfs_schema_dir)
if commStatus is not 0:
    logging.info('Upload all the .avsc schema file.')
    logging.info('hdfs dfs -put %s/java_code/*.avsc %s', workhome, hdfs_schema_dir)
    os.system('hdfs dfs -put %s/java_code/*.avsc %s' % (workhome, hdfs_schema_dir))

# backup
logging.info('Check if the backup tar.gz file has generated in the local server...')
commStatus = os.system('[ -e %s ]' % local_schema_backup_filename)
if commStatus is not 0:
    logging.info('package and compress the schema files')
    logging.info('tar -czf %s ./java_code/*.avsc', local_schema_backup_filename)
    os.system('tar -czf %s ./java_code/*.avsc' % local_schema_backup_filename)

logging.info('Check if the backup tar.gz file has upload to the HDFS...')
commStatus = os.system('hdfs dfs -test -e %s > /dev/null' % hdfs_schema_backup_filename)
if commStatus is not 0:
    logging.info('upload the schema package file to HDFS')
    logging.info('hdfs dfs -put %s %s', local_schema_backup_filename, hdfs_schema_backup_filename)
    os.system('hdfs dfs -put %s %s' %(local_schema_backup_filename, hdfs_schema_backup_filename))

```



- HDFS数据验证

  - 统一风格

    - 路径名小写
    - 文件名小写

    ![image-20210211011021238](https://s2.loli.net/2022/05/19/TCcYBZQFW9nEPSa.png)

