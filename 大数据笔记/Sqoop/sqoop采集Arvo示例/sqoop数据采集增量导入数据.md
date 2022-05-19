# 增量导入数据

## 在/opt/sqoop/one_make下创建一个incr_import_tables.txt文件，里面保存了所有需要导入的表

```shell
touch /opt/sqoop/one_make/incr_import_tables.txt
vim /opt/sqoop/one_make/incr_import_tables.txt

ciss4.ciss_csp_m_bnblp_hx_sqd
ciss4.ciss_csp_m_bnblp_hx_sqd_dtl
ciss4.ciss_csp_m_bnlp_hx_sqd
ciss4.ciss_csp_m_bnlp_hx_sqd_dtl
ciss4.ciss_csp_m_wl_db_sqd
ciss4.ciss_csp_m_wl_db_sqd_dtl
ciss4.ciss_csp_m_wl_sqd
ciss4.ciss_csp_m_wl_sqd_dtl
ciss4.ciss_csp_m_xhp_hx_sqd
ciss4.ciss_csp_m_xhp_hx_sqd_dtl
ciss4.ciss_csp_m_xhp_sqd
ciss4.ciss_csp_m_xhp_sqd_dtl
ciss4.ciss_csp_workorder
ciss4.ciss_csp_workorder_device
ciss4.ciss_material_bnblp_hx_sqd
ciss4.ciss_material_bnblp_hx_sqd_dtl
ciss4.ciss_material_bnlp_hx_sqd
ciss4.ciss_material_bnlp_hx_sqd_dtl
ciss4.ciss_material_sx_repair_dtl
ciss4.ciss_material_sx_sqd
ciss4.ciss_material_sx_sqd_dtl
ciss4.ciss_material_wdwl_db_sqd
ciss4.ciss_material_wdwl_db_sqd_dtl
ciss4.ciss_material_wdwl_sqd
ciss4.ciss_material_wdwl_sqd_dtl
ciss4.ciss_material_wdwl_sq_dtl_seq
ciss4.ciss_material_wldzmx_sqd
ciss4.ciss_material_xhp_hx_sqd
ciss4.ciss_material_xhp_hx_sqd_dtl
ciss4.ciss_material_xhp_sqd
ciss4.ciss_material_xhp_sqd_dtl
ciss4.ciss_service_callaccept
ciss4.ciss_service_changeuser_record
ciss4.ciss_service_cstm_evaluation
ciss4.ciss_service_exchanged_m_dtl
ciss4.ciss_service_expense_report
ciss4.ciss_service_exp_report_dtl
ciss4.ciss_service_fault_dtl
ciss4.ciss_service_inspection
ciss4.ciss_service_install
ciss4.ciss_service_install_validate
ciss4.ciss_service_order
ciss4.ciss_service_order_device
ciss4.ciss_service_other
ciss4.ciss_service_remould
ciss4.ciss_service_repair
ciss4.ciss_service_repaired_m_dtl
ciss4.ciss_service_return_visit
ciss4.ciss_service_travel_expense
ciss4.ciss_service_trvl_exp_dtl
ciss4.ciss_service_trvl_exp_sum
ciss4.ciss_service_workorder
ciss4.ciss_service_workorder_back
ciss4.ciss_service_workorder_user
ciss4.ciss_s_exp_report_wo_payment
ciss4.ciss_s_install_exp_report
ciss4.ciss_s_install_exp_report_dtl
ciss_s_install_exp_rep_02_dtl
```

## 创建sqoop全量导入shell(python)脚本文件

```shell
touch /opt/sqoop/one_make/incr_import_tables.sh
chmod a+x /opt/sqoop/one_make/incr_import_tables.sh
vim /opt/sqoop/one_make/incr_import_tables.sh
```

## 读取该文件并进行遍历

```shell
#!/usr/bin/env bash
# 编写SHELL脚本的时候要特别小心，特别是编写SQL的条件，如果中间加了空格，就会导致命令执行失败
# /bin/bash
biz_date=20210101
biz_fmt_date=2021-01-01
dw_parent_dir=/data/dw/ods/one_make/incr_imp
workhome=/opt/sqoop/one_make
incr_imp_tables=${workhome}/incr_import_tables.txt

orcl_srv=oracle.bigdata.cn
orcl_port=1521
orcl_sid=helowin
orcl_user=ciss
orcl_pwd=123456

mkdir ${workhome}/log

sqoop_condition_params="--where \"'${biz_fmt_date}'=to_char(CREATE_TIME,'yyyy-mm-dd')\""
sqoop_import_params="sqoop import -Dmapreduce.job.user.classpath.first=true --outdir ${workhome}/java_code --as-avrodatafile"
sqoop_jdbc_params="--connect jdbc:oracle:thin:@${orcl_srv}:${orcl_port}:${orcl_sid} --username ${orcl_user} --password ${orcl_pwd}"

# load hadoop/sqoop env
source /etc/profile

while read p; do
    # clean old directory in HDFS
    hdfs dfs -rm -r ${dw_parent_dir}/${p}/${biz_date}
    
    # parallel execution import
    ${sqoop_import_params} ${sqoop_jdbc_params} --target-dir ${dw_parent_dir}/${p}/${biz_date} --table ${p^^} ${sqoop_condition_params} -m 1 &
    cur_time=`date "+%F %T"`
    echo "${cur_time}: ${sqoop_import_params} ${sqoop_jdbc_params} --target-dir ${dw_parent_dir}/${p,,}/${biz_date} --table ${p} ${sqoop_condition_params} -m 1 &" >> ${workhome}/log/${biz_fmt_date}_incr_imp.log
    sleep 15
    
done < ${incr_imp_tables}
```

------

```python
#!/usr/bin/env python
# @Time : 2021/7/20 15:19
# @desc :
__coding__ = "utf-8"
__author__ = "itcast"

import os
import subprocess
import datetime
import time
import logging

biz_date = '20210101'
biz_fmt_date = '2021-01-01'
dw_parent_dir = '/data/dw/ods/one_make/incr_imp'
workhome = '/opt/sqoop/one_make'
incr_imp_tables = workhome + '/incr_import_tables.txt'
if os.path.exists(workhome + '/log'):
    os.system('make ' + workhome + '/log')

orcl_srv = 'oracle.bigdata.cn'
orcl_port = '1521'
orcl_sid = 'helowin'
orcl_user = 'ciss'
orcl_pwd = '123456'

sqoop_import_params = 'sqoop import -Dmapreduce.job.user.classpath.first=true --outdir %s/java_code --as-avrodatafile' % workhome
sqoop_jdbc_params = '--connect jdbc:oracle:thin:@%s:%s:%s --username %s --password %s' % (orcl_srv, orcl_port, orcl_sid, orcl_user, orcl_pwd)

# load hadoop/sqoop env
subprocess.call("source /etc/profile", shell=True)
print('executing...')
# read file
fr = open(incr_imp_tables)
for line in fr.readlines():
    tblName = line.rstrip('\n')
    # clean old directory in HDFS
    hdfs_command = 'hdfs dfs -rm -r %s/%s/%s' % (dw_parent_dir, tblName, biz_date)
    # parallel execution import
    # ${sqoop_import_params} ${sqoop_jdbc_params} --target-dir ${dw_parent_dir}/${p}/${biz_date} --table ${p^^} -m 1 &
    # sqoopImportCommand = f''' {sqoop_import_params} {sqoop_jdbc_params} --target-dir {dw_parent_dir}/{tblName}/{biz_date} --table {tblName.upper()} -m 1 &'''
    sqoopImportCommand = '''
    %s %s --target-dir %s/%s/%s --table %s -m 1 &
    ''' % (sqoop_import_params, sqoop_jdbc_params, dw_parent_dir, tblName, biz_date, tblName.upper())
    # parallel execution import
    subprocess.call(sqoopImportCommand, shell=True)
    # cur_time=`date "+%F %T"`
    # cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.basicConfig(level=logging.INFO,
                        filename='%s/log/%s_full_imp.log' % (workhome, biz_fmt_date),
                        filemode='a',
                        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # logging.info(cur_time + ' : ' + sqoopImportCommand)
    logging.info(sqoopImportCommand)
    time.sleep(15)

```



## 执行脚本测试

`/opt/sqoop/one_make/incr_import_tables.sh` 或

`/opt/sqoop/one_make/incr_import_tables.py`

![image-20210211002414440](https://s2.loli.net/2022/05/19/PDCA1eKbFwhmyta.png)

## 等待导入数据全部成功，查看导入情况

- 到hdfs的/data/dw/ods/one_make/incr_imp目录下查看增量表导入情况

