# 全量导入数据

## 启动容器

`docker start mysql oracle hadoop sqoop`

## 从oracle数据库拷贝需要的表名

- 使用dbeaver选择所有以CISS的表，右键点击复制高级信息，即可复制出来所有的表名

  ![image-20210210233744879](https://s2.loli.net/2022/05/19/ZfQkqJNgUWMwLxV.png)

- 表名

  ```
  CISS4.CISS_ADMIN_EXCEPTION_LOG
  CISS4.CISS_ADMIN_SYS_UPDATE_LOG
  CISS4.CISS_APPROVE_DTL
  CISS4.CISS_BASE_ACCOUNTINGITEM
  CISS4.CISS_BASE_AREAS
  CISS4.CISS_BASE_BASEINFO
  CISS4.CISS_BASE_BTN_ROLE
  CISS4.CISS_BASE_BTN_ROLE_DTL
  CISS4.CISS_BASE_BZKCGL
  CISS4.CISS_BASE_BZKCGL_DTL
  CISS4.CISS_BASE_CSP
  CISS4.CISS_BASE_CUSTOMER
  CISS4.CISS_BASE_DEVICE
  CISS4.CISS_BASE_DEVICE_DETAIL
  CISS4.CISS_BASE_DEVICE_DETAIL_0926
  CISS4.CISS_BASE_DEVICE_FACTORY_INFO
  CISS4.CISS_BASE_DEVICE_MODEL
  CISS4.CISS_BASE_DEVICE_NAME
  CISS4.CISS_BASE_DEVICE_SYS_DEF_FAC
  CISS4.CISS_BASE_DEVICE_TYPE
  CISS4.CISS_BASE_FAULT_CATEGORY
  CISS4.CISS_BASE_MATERIAL
  CISS4.CISS_BASE_MATERIAL_DETAIL
  CISS4.CISS_BASE_NOBUSINESS_SUBSIDY
  CISS4.CISS_BASE_NO_SUBSIDY_TEMP
  CISS4.CISS_BASE_OILSTATION
  CISS4.CISS_BASE_OILSTATION_CONTRACT
  CISS4.CISS_BASE_OILSTATION_USER
  CISS4.CISS_BASE_REASONCODE
  CISS4.CISS_BASE_SERVICESTATION
  CISS4.CISS_BASE_SUBSIDY
  CISS4.CISS_BASE_SUB_ACCOUNITEM
  CISS4.CISS_BASE_WAREHOUSE
  CISS4.CISS_BASE_WAREHOUSE_LOCATION
  CISS4.CISS_BIZ_ERP_TASK
  CISS4.CISS_CSP_DEVICE_CATEGORY_MONEY
  CISS4.CISS_CSP_DEVICE_FAULT
  CISS4.CISS_CSP_DEVICE_INST_MONEY
  CISS4.CISS_CSP_EXCHANGED_M_DTL
  CISS4.CISS_CSP_M_BNBLP_HX_SQD
  CISS4.CISS_CSP_M_BNBLP_HX_SQD_DTL
  CISS4.CISS_CSP_M_BNLP_HX_SQD
  CISS4.CISS_CSP_M_BNLP_HX_SQD_DTL
  CISS4.CISS_CSP_M_WL_DB_SQD
  CISS4.CISS_CSP_M_WL_DB_SQD_DTL
  CISS4.CISS_CSP_M_WL_SQD
  CISS4.CISS_CSP_M_WL_SQD_1
  CISS4.CISS_CSP_M_WL_SQD_DTL
  CISS4.CISS_CSP_M_WL_SQD_DTL_1
  CISS4.CISS_CSP_M_XHP_HX_SQD
  CISS4.CISS_CSP_M_XHP_HX_SQD_DTL
  CISS4.CISS_CSP_M_XHP_SQD
  CISS4.CISS_CSP_M_XHP_SQD_1
  CISS4.CISS_CSP_M_XHP_SQD_DTL
  CISS4.CISS_CSP_M_XHP_SQD_DTL_1
  CISS4.CISS_CSP_OIL_STATION
  CISS4.CISS_CSP_OIL_STATION_DEVICE
  CISS4.CISS_CSP_REPAIR_MATERIAL
  CISS4.CISS_CSP_WAREHOUSE_CODE
  CISS4.CISS_CSP_WORKORDER
  CISS4.CISS_CSP_WORKORDER_DEVICE
  CISS4.CISS_DAYS
  CISS4.CISS_DEVICE_INST_MONEY
  CISS4.CISS_ENTRIPRISE_WECHAT_ASSIGN
  CISS4.CISS_ERP_OPERATION_RESULT
  CISS4.CISS_EXPENSE_SUBSIDY
  CISS4.CISS_FAULT_HOUR
  CISS4.CISS_IM_ASSETS
  CISS4.CISS_IM_ASSETS_RECORD
  CISS4.CISS_IM_ASSETS_USE
  CISS4.CISS_IM_BUSINESS_TRVL_SQD
  CISS4.CISS_IM_CAR
  CISS4.CISS_IM_EXPENSE_REPORT
  CISS4.CISS_IM_EXPENSE_REPORT_DTL
  CISS4.CISS_IM_FRINGE_BENEFIT
  CISS4.CISS_IM_OFFICE_SUPPLIES_DTL
  CISS4.CISS_IM_OFFICE_SUPPLIES_SQD
  CISS4.CISS_IM_PERSON_TRANSFER
  CISS4.CISS_IM_SALARY_DTL
  CISS4.CISS_IM_SALSEMANAGER
  CISS4.CISS_IM_SALSEMMANAGER_DTL
  CISS4.CISS_IM_TRAINING_SQD
  CISS4.CISS_IM_TRANS_HISTORY
  CISS4.CISS_IM_VACATION
  CISS4.CISS_IM_VEHICLE
  CISS4.CISS_IM_VEHICLE_SQD
  CISS4.CISS_KB_TAG
  CISS4.CISS_MATERIAL_BNBLP_HX_SQD
  CISS4.CISS_MATERIAL_BNBLP_HX_SQD_1
  CISS4.CISS_MATERIAL_BNBLP_HX_SQD_DTL
  CISS4.CISS_MATERIAL_BNLP_HX_SQD
  CISS4.CISS_MATERIAL_BNLP_HX_SQD_1
  CISS4.CISS_MATERIAL_BNLP_HX_SQD_DTL
  CISS4.CISS_MATERIAL_SX_REPAIR_DTL
  CISS4.CISS_MATERIAL_SX_SQD
  CISS4.CISS_MATERIAL_SX_SQD_1
  CISS4.CISS_MATERIAL_SX_SQD_DTL
  CISS4.CISS_MATERIAL_SX_SQD_DTL_1
  CISS4.CISS_MATERIAL_WDWL_DB_SQD
  CISS4.CISS_MATERIAL_WDWL_DB_SQD_1
  CISS4.CISS_MATERIAL_WDWL_DB_SQD_DTL
  CISS4.CISS_MATERIAL_WDWL_DB_SQD_DTL1
  CISS4.CISS_MATERIAL_WDWL_SQD
  CISS4.CISS_MATERIAL_WDWL_SQD_1
  CISS4.CISS_MATERIAL_WDWL_SQD_DTL
  CISS4.CISS_MATERIAL_WDWL_SQ_DTL_SEQ
  CISS4.CISS_MATERIAL_WDWL_VIRTUAL
  CISS4.CISS_MATERIAL_WDWL_VIRTUAL_DTL
  CISS4.CISS_MATERIAL_WLDZMX_SQD
  CISS4.CISS_MATERIAL_XHP_HX_SQD
  CISS4.CISS_MATERIAL_XHP_HX_SQD_1
  CISS4.CISS_MATERIAL_XHP_HX_SQD_DTL
  CISS4.CISS_MATERIAL_XHP_SQD
  CISS4.CISS_MATERIAL_XHP_SQD_1
  CISS4.CISS_MATERIAL_XHP_SQD_DTL
  CISS4.CISS_MKT_CONTRACT
  CISS4.CISS_MKT_DEMAND_RESEARCH_LIST
  CISS4.CISS_MKT_QUESTION_ANSWER
  CISS4.CISS_MKT_RESEARCH_QUESTION
  CISS4.CISS_MKT_SALES_ORDER
  CISS4.CISS_MKT_SALES_ORDER_DTL
  CISS4.CISS_MKT_SALES_PLAN
  CISS4.CISS_MKT_SALES_PLAN_DTL
  CISS4.CISS_M_BNBLP_HX_SQD_DTL_1
  CISS4.CISS_M_BNLP_HX_SQD_DTL_1
  CISS4.CISS_M_MANUAL_DB
  CISS4.CISS_M_MANUAL_DB_DTL
  CISS4.CISS_M_WDWL_DB_SQD_DTL_1
  CISS4.CISS_M_WDWL_SQD_DTL_1
  CISS4.CISS_M_XHP_HX_SQD_DTL_1
  CISS4.CISS_M_XHP_SQD_DTL_1
  CISS4.CISS_R_DEVICE_DTL_BIZ
  CISS4.CISS_R_SERSTATION_WAREHOUSE
  CISS4.CISS_R_WF_BUSS
  CISS4.CISS_SERVICE_CALLACCEPT
  CISS4.CISS_SERVICE_CHANGEUSER_RECORD
  CISS4.CISS_SERVICE_CSTM_EVALUATION
  CISS4.CISS_SERVICE_EXCHANGED_M_DTL
  CISS4.CISS_SERVICE_EXPENSE_REPORT
  CISS4.CISS_SERVICE_EXPENSE_REPORT_1
  CISS4.CISS_SERVICE_EXP_REPORT_DTL
  CISS4.CISS_SERVICE_EXP_REPORT_DTL_1
  CISS4.CISS_SERVICE_FAULT_DTL
  CISS4.CISS_SERVICE_INSPECTION
  CISS4.CISS_SERVICE_INSTALL
  CISS4.CISS_SERVICE_INSTALL_DEVICE
  CISS4.CISS_SERVICE_INSTALL_VALIDATE
  CISS4.CISS_SERVICE_INSTALL_VISIT
  CISS4.CISS_SERVICE_ORDER
  CISS4.CISS_SERVICE_ORDER_DEVICE
  CISS4.CISS_SERVICE_OTHER
  CISS4.CISS_SERVICE_REMOULD
  CISS4.CISS_SERVICE_REPAIR
  CISS4.CISS_SERVICE_REPAIRED_M_DTL
  CISS4.CISS_SERVICE_RETURN_VISIT
  CISS4.CISS_SERVICE_TRAVEL_EXPENSE
  CISS4.CISS_SERVICE_TRVL_EXP_DTL
  CISS4.CISS_SERVICE_TRVL_EXP_SUM
  CISS4.CISS_SERVICE_TRVL_EXP_SUM_DTL
  CISS4.CISS_SERVICE_WORKORDER
  CISS4.CISS_SERVICE_WORKORDER_BACK
  CISS4.CISS_SERVICE_WORKORDER_REMARK
  CISS4.CISS_SERVICE_WORKORDER_USER
  CISS4.CISS_SPT_ANNOUNCEMENT
  CISS4.CISS_SPT_ANSWER_SHEET
  CISS4.CISS_SPT_ANSWER_SHEET_DTL
  CISS4.CISS_SPT_CENETS_SPT_SQD
  CISS4.CISS_SPT_KB_ARTICLE
  CISS4.CISS_SPT_KB_ARTICLE_CATEGORY
  CISS4.CISS_SPT_KB_ARTICLE_TAG
  CISS4.CISS_SPT_KB_CATEGORY
  CISS4.CISS_SPT_QL_CATEGORY
  CISS4.CISS_SPT_QL_QUESTION_CATEGORY
  CISS4.CISS_SPT_QUALITY_ISSUE
  CISS4.CISS_SPT_QUALITY_ISSUE_TASK
  CISS4.CISS_SPT_TEST_PAPER
  CISS4.CISS_SPT_TEST_PAPER_DTL
  CISS4.CISS_SPT_TEST_PAPER_PARTINER
  CISS4.CISS_SPT_TEST_QUESTION
  CISS4.CISS_SYSTEM_LOG
  CISS4.CISS_S_DEVICE_INSTALL_TYPE
  CISS4.CISS_S_EXP_REPORT_WO_PAYMENT
  CISS4.CISS_S_INSTALL_EXP_REPORT
  CISS4.CISS_S_INSTALL_EXP_REPORT_1
  CISS4.CISS_S_INSTALL_EXP_REPORT_DTL
  CISS4.CISS_S_INSTALL_EXP_REPORT_DTL_
  CISS4.CISS_S_INSTALL_EXP_REP_02
  CISS4.CISS_S_INSTALL_EXP_REP_02_1
  CISS4.CISS_S_INSTALL_EXP_REP_02_DTL
  CISS4.CISS_S_INSTALL_EXP_REP_02_DTL_
  CISS4.CISS_TMP_BASE_OILSTATION
  CISS4.CISS_TMP_BASE_OILSTATION_USER
  CISS4.CISS_TMP_EXCHANGE_DTL_C
  CISS4.CISS_TMP_OIL_STATION_CODE
  CISS4.CISS_TMP_OIL_STATION_CONTACT
  CISS4.CISS_TMP_OIL_STATION_EXCL
  CISS4.CISS_USER_CALL_CENTER_USER
  CISS4.CISS_WDWL_SX_DTL_SEQ
  CISS4.CISS_WEIXIN_REPAIR
  ```

- 然后用Excel来做全量表和增量表的划分。相当于使用Excel来进行表名的过滤、筛选

  - 1.创建一个Excel文件，在sheet中创建两个列，一个列为全量导入、一个列为增量导入
  - 2.将所有的表名复制到全量导入中。然后我们根据表的业务性质从全量导入移动到增量导入中

- 判断原则：业务性质的表使用增量导入、基础数据性质的表使用全量导入，如果数仓中无需使用，直接在Excel中删除该表。最后得出本次全量导入：44张表、增量导入58张表。

## 调整yarn容量调度配置

### 查看最小调度单位

- 为了能够并行的执行多个任务，我们需要调整下`yarn-site.xml`的调度器配置

  `yarn.scheduler.capacity.maximum-am-resource-percent`，该参数的意义集群中可用于运行application master的资源比例上限，这通常用于限制并发运行的应用程序数目。默认是0.1，简单来理解就是AM能够使用的资源最大不能超过YARN管理的资源的10%，我们当前的内存是8G，0.1相当于能使用的也就是不到1G，而YARN配置的**最小调度单元是1G**。

- 为了提高JOB的并发量，把AM的占比调整为0.8。

- 操作

  ```shell
  docker exec -it hadoop bash
  # 进入hadoop容器后编辑yarn配置文件
  source /etc/profile
  vim ${HADOOP_HOME}/etc/hadoop/yarn-site.xml
  ```

  ```xml
  <property>
      <name>yarn.scheduler.minimum-allocation-mb</name>
      <value>512</value>
  </property>
  <property>
          <name>yarn.nodemanager.pmem-check-enabled</name>
          <value>false</value>
  </property>
  <property>
          <name>yarn.nodemanager.vmem-check-enabled</name>
          <value>false</value>
  </property>
  <property>
          <name>yarn.nodemanager.resource.memory-mb</name>
          <value>16384</value>
  </property>
  ```

  ```xml
  <!-- vim ${HADOOP_HOME}/etc/hadoop/capacity-scheduler.xml -->
  <property>
      <name>yarn.scheduler.capacity.maximum-am-resource-percent</name>
      <value>0.8</value>
  </property>
  ```

- 修改完配置后重启yarn

  ```shell
  stop-yarn.sh
  start-yarn.sh
  ```

- 在YARN的webui中可以查看到最小调度单元变成了512M

  ![image-20210210234435195](https://s2.loli.net/2022/05/19/kYTJE5zaDpQMyIG.png)



### 查看AM最大允许使用资源

- 点击YARN WEB UI上的scheduler，我们可以查看到当前队列中的配置。可以看到，当前AM的最大内存容量为6656。这样就可以同时运行多个sqoop的job。

![image-20210210234533073](https://s2.loli.net/2022/05/19/7QeYtUZRnC3hWq9.png)

- 更多详细配置请大家参考Hadoop官方文档：https://hadoop.apache.org/docs/r2.7.0/

## 开启MapReduce的uber模式

- 在Sqoop运行作业时，我们可以注意到每一个Job会打印当前是否运行在uber模式。

  ```properties
  20/12/25 04:28:14 INFO mapreduce.Job: Job job_1608863644443_0103 running in uber mode : false
  20/12/25 04:28:14 INFO mapreduce.Job:  map 0% reduce 0%
  20/12/25 04:28:18 INFO mapreduce.Job:  map 100% reduce 0%
  ```

- 当前，我们需要导入的有100多张，执行每个sqoop命令都需要启动一个MapReduce程序，重新向ResourceManager申请资源，然后启动Application Master，AM再申请资源启动Container运行MapTask和ReduceTask。而每次创建Container其实就是启动一个JVM虚拟机。

- 针对这些小作业，如果我们直接每个任务都只运行在一个AM Container中，这样比起AM向RM申请资源，然后NM再启动、关闭资源要高效很多。当然这就要求，作业要足够的“小”。

- 基于上述场景，我们可以使用Uber模式（超级任务）来优化这些小作业。这种方式，会在一个JVM中顺序执行这些小作业。我们可以通过参数来配置最大的MapTask数量（默认9个）、最大的Reduce数量（默认1个）、以及最大的数据量大小（默认大小是一个Block的大小）。

- uber模式相关说明：https://hadoop.apache.org/docs/r2.7.0/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml

- 注意，但我们配置Uber模式的时候，需要按照以下规则：

  - 1. `yarn.app.mapreduce.am.resource.mb`必须大于`mapreduce.map.memory.mb`和`mapreduce.reduce.memory.mb`
    2. `yarn.app .mapreduce.am.resource.cpu-vcores`必须大于`mapreduce.map.cpu.vcores`和`mapreduce.map.cpu.vcores`

- 查看当前yarn的AM的配置:

  - 在scheulder页面中，我们可以看到AM的配置最大可以是：13G、1个vcore。

     ![image-20210210235200337](https://s2.loli.net/2022/05/19/FdAnLRyHjqQ3sU6.png)

  - 而MapTask和ReduceTask的配置如下：

    ```xml
    <property>
      <name>mapreduce.map.memory.mb</name>
      <value>1024</value>
      <source>mapred-default.xml</source>
    </property>
    <property>
      <name>mapreduce.reduce.memory.mb</name>
      <value>1024</value>
      <source>mapred-default.xml</source>
    </property>
    <property>
      <name>mapreduce.map.cpu.vcores</name>
      <value>1</value>
      <source>mapred-default.xml</source>
    </property>
    <property>
      <name>mapreduce.reduce.cpu.vcores</name>
      <value>1</value>
      <source>mapred-default.xml</source>
    </property>
    ```

  - 说明，当前的配置是可以支持Uber模式的。所以，接下来，我们来配置Uber模式。我们只需要把mapred-site.xml中加入以下配置即可。

    ```xml
    <property>
      <name>mapreduce.job.ubertask.enable</name>
      <value>true</value>
    </property>
    ```

  - 重启yarn，使uber模式生效

## 编写sqoop命令执行导入

### 测试全量导入数据

- 找到一个全量表来测试，先跑通一条命令，然后再编写SHELL脚本来进行导入所有全量表。

  执行以下SQOOP脚本，因为当前docker中只有一个NM，所以，我们就使用一个maptask来执行。

  ```shell
  sqoop import --connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin --username ciss --password 123456 --target-dir /data/dw/ods/one_make/full_imp/CISS4.CISS_BASE_AREAS/20210101 --fields-terminated-by "\001" --table CISS4.CISS_BASE_AREAS -m 1
  ```

- 通过webui我们可以查看到JOB的运行情况

  ![image-20210210235517684](https://s2.loli.net/2022/05/19/ByCjQSpsYKLXHvm.png)

- 数据均能正确导出，一共为47562条数据。通过观察数据文件我们发现，表中为空的字段被处理为null字符串了。

  ![image-20210210235536729](https://s2.loli.net/2022/05/19/2UORwLMyoa98ZD1.png)

- 重跑需要清除下分区文件夹：

  `hdfs dfs -rm -r /data/dw/ods/one_make/full_imp/CISS4.CISS_BASE_AREAS/20210101`

### 解决文件数据问题

- 其实上面的数据看起来是没有什么问题的，但我们往下看，能看到一些非常严重的问题。就是数据字段映射出错！

  ![image-20210210235625966](https://s2.loli.net/2022/05/19/rGXgYyLot2DuRZb.png)

- 一些数据中有\n，换行符。这个问题如果不处理，就会导致我们导入到Hive中数据字段映射都是错的。会出现大量为NULL的数据。因为Hive是以\n换行符来分隔行的。

- 解决这个问题，有两种方案

  - 1. 在sqoop中增加，--hive-drop-import-delims ，这个配置会在导入数据到HDFS时，自动处理hive的分隔符。也就是将一些换行符处理掉。但这种方式，会影响数据，也就是将来我们做提数的时候，一些数据格式将会出现混乱
  - 2. 使用Avro方式来保存数据。因为Avro的数据是二进制数据，而且是自带Schema的。就是一份数据的结构是能够通过schema映射出来。而且Avro数据存储更紧凑。使用Avro存储可以完美解决上述问题。

- 我们需要对sqoop命令做以下调整

  ```shell
  hdfs dfs -rm -r -skipTrash /data/dw/ods/one_make/incr_imp/CISS4.CISS_SERVICE_WORKORDER
  hdfs dfs -mkdir -p /data/dw/ods/one_make/incr_imp/CISS4.CISS_SERVICE_WORKORDER
  
  sqoop import \
  -Dmapreduce.job.user.classpath.first=true \
  --connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
  --username ciss \
  --password 123456 \
  --target-dir /data/dw/ods/one_make/incr_imp/CISS4.CISS_SERVICE_WORKORDER/20210101 \
  --where "'2021-01-01'=to_char(CREATE_TIME ,'yyyy-mm-dd')" \
  --table CISS4.CISS_SERVICE_WORKORDER \
  --as-avrodatafile \
  -m 1
  ```

- 我们增加了一行--as-avrodatafile配置，表示当前用sqoop输出的就是Avro文件格式的数据文件。

  - 注意：前面还需要加上一个-Dmapreduce.job.user.classpath.first=true，否则运行sqoop的时候会抛出找不到Avro类库的问题。
  - 重新运行sqoop脚本，我们发现，现在的文件大小也比文本方式小了。只有94M，相当于节省了30多M的空间。 

  > 后续我们都将使用这种方式来导出。

### 编写shell(或python)脚本进行全量导入

- 开始编写脚本来将所有表进行全量导入

  - sqoop参考命令

    ```shell
  sqoop import \
    -Dmapreduce.job.user.classpath.first=true \
    --as-avrodatafile \
    --connect jdbc:oracle:thin:@oracle.bigdata.cn:1521:helowin \
    --username ciss \
    --password 123456 \
    --target-dir /data/dw/ods/one_make/full_imp/CISS4.CISS_SERVICE_WORKORDER/20210101 \
    --table CISS4.CISS_SERVICE_WORKORDER \
    --outdir /opt/sqoop/one_make/java_code
    -m 1
    ```
  
  1. 在/opt/sqoop/one_make下创建一个full_import_tables.txt文件，里面保存了所有需要导入的表
  
     ```shell
     mkdir -p /opt/sqoop/one_make
     touch /opt/sqoop/one_make/full_import_tables.txt
     
     vim /opt/sqoop/one_make/full_import_tables.txt
     ciss4.ciss_base_areas
     ciss4.ciss_base_baseinfo
     ciss4.ciss_base_csp
     ciss4.ciss_base_customer
     ciss4.ciss_base_device
     ciss4.ciss_base_device_detail
     ciss4.ciss_base_device_factory_info
     ciss4.ciss_base_device_model
     ciss4.ciss_base_device_name
     ciss4.ciss_base_device_sys_def_fac
     ciss4.ciss_base_device_type
     ciss4.ciss_base_fault_category
     ciss4.ciss_base_material
     ciss4.ciss_base_material_detail
     ciss4.ciss_base_nobusiness_subsidy
     ciss4.ciss_base_no_subsidy_temp
     ciss4.ciss_base_oilstation
     ciss4.ciss_base_oilstation_contract
     ciss4.ciss_base_oilstation_user
     ciss4.ciss_base_reasoncode
     ciss4.ciss_base_servicestation
     ciss4.ciss_base_subsidy
     ciss4.ciss_base_sub_accounitem
     ciss4.ciss_base_warehouse
     ciss4.ciss_base_warehouse_location
     ciss4.ciss_csp_device_category_money
     ciss4.ciss_csp_device_fault
     ciss4.ciss_csp_device_inst_money
     ciss4.ciss_csp_exchanged_m_dtl
     ciss4.ciss_csp_oil_station
  ciss4.ciss_csp_oil_station_device
     ciss4.ciss_csp_warehouse_code
  ciss4.ciss_device_inst_money
     ciss4.ciss_fault_hour
     ciss4.ciss_r_serstation_warehouse
     ciss4.ciss_s_device_install_type
     ciss4.ciss_user_call_center_user
     ciss4.eos_dict_entry
  ciss4.eos_dict_type
     ciss4.org_employee
  ciss4.org_emporg
     ciss4.org_empposition
  ciss4.org_organization
     ciss4.org_position
     ```
   ```
  
   ```
2. 创建sqoop全量导入shell脚本文件
  
   ```shell
     touch /opt/sqoop/one_make/full_import_tables.sh
   chmod a+x /opt/sqoop/one_make/full_import_tables.sh
     vim /opt/sqoop/one_make/full_import_tables.sh
   ```
  
3. 读取该文件并进行遍历
  
   a) 创建基础变量：
  
   ​	i. biz_date：目录日期格式（yyyyMMdd）
  
   ​	ii. biz_fmt_date：日期日志格式（yyyy-MM-dd）
  
   ​	iii. dw_parent_dir：全量导入父目录
  
   ​	iv. workhome：sqoop的项目home目录
  
   ​	v. full_imp_tables：全量表文件全路径
  
   b) 创建日志目录：
  
   ​	i. 基于sqoop项目home目录
  
   c) 创建orcale数据库odbc连接变量
  
   ​	i. orcl_srv：oracle连接地址(host或ip)
  
   ​	ii. orcl_port：端口
  
   ​	iii. orcl_sid：service名称
  
   ​	iv. orcl_user：用户名
  
   ​	v. orcl_pwd：密码
  
   d) 定义sqoop导入命令
  
   ​	i. sqoop_import_params：定义sqoop导入参数变量（包含：job参数、代码输出路径）
  
   ​	ii. sqoop_jdbc_params：定义sqoop导入oracle参数变量（包含：连接、用户名、密码）
  
     e) 执行sqoop导入之前，加载hadoop、sqoop环境变量
  
     f) 根据表名，循环执行sqoop导入
  
     ​	i. 后台执行sqoop导入命令
  
     ​	ii. 定义获得当前时间的变量：cur_time
  
     ​	iii. 记录时间和命令日志，并写入到日志目录下
  
     ​		1.规则：时间(yyyy-MM-dd HH:mm:ss):sqoop命令，最终追加到日志文件中
  
     ​		2.为避免oracle崩溃，执行一次sqoop导入命令，睡眠15秒
  
     ```shell
     #!/usr/bin/env bash
     # /bin/bash
     biz_date=20210101
     biz_fmt_date=2021-01-01
     dw_parent_dir=/data/dw/ods/one_make/full_imp
     workhome=/opt/sqoop/one_make
     full_imp_tables=${workhome}/full_import_tables.txt
     
     mkdir ${workhome}/log
     
     orcl_srv=oracle.bigdata.cn
     orcl_port=1521
     orcl_sid=helowin
     orcl_user=ciss
     orcl_pwd=123456
   
     sqoop_import_params="sqoop import -Dmapreduce.job.user.classpath.first=true --outdir ${workhome}/java_code --as-avrodatafile"
   sqoop_jdbc_params="--connect jdbc:oracle:thin:@${orcl_srv}:${orcl_port}:${orcl_sid} --username ${orcl_user} --password ${orcl_pwd}"
     
   # load hadoop/sqoop env
     source /etc/profile
   
     while read p; do
       # parallel execution import
         ${sqoop_import_params} ${sqoop_jdbc_params} --target-dir ${dw_parent_dir}/${p}/${biz_date} --table ${p^^} -m 1 &
       cur_time=`date "+%F %T"`
         echo "${cur_time}: ${sqoop_import_params} ${sqoop_jdbc_params} --target-dir ${dw_parent_dir}/${p}/${biz_date} --table ${p} -m 1 &" >> ${workhome}/log/${biz_fmt_date}_full_imp.log
       sleep 15
     done < ${full_imp_tables}
     ```
  
   ------
   
   ```python
   !/usr/bin/env python
   
     coding = "utf-8"
     author = "itcast"
   
     import os
     import subprocess
     import datetime
     import time
     import logging
   
     biz_date = '20210101'
     biz_fmt_date = '2021-01-01'
     dw_parent_dir = '/data/dw/ods/one_make/full_imp'
     workhome = '/opt/sqoop/one_make'
     full_imp_tables = workhome + '/full_import_tables.txt'
     if os.path.exists(workhome + '/log'):
         os.system('make ' + workhome + '/log')
   
     orcl_srv = 'oracle.bigdata.cn'
     orcl_port = '1521'
     orcl_sid = 'helowin'
     orcl_user = 'ciss'
     orcl_pwd = '123456'
   
     sqoop_import_params = 'sqoop import -Dmapreduce.job.user.classpath.first=true --outdir %s/java_code --as-avrodatafile' % workhome
     sqoop_jdbc_params = '--connect jdbc:oracle:thin:@%s:%s:%s --username %s --password %s' % (orcl_srv, orcl_port, orcl_sid, orcl_user, orcl_pwd)
   
   load hadoop/sqoop env
   
     subprocess.call("source /etc/profile", shell=True)
     print('executing...')
   
   read file
   
     fr = open(full_imp_tables)
     for line in fr.readlines():
         tblName = line.rstrip('\n')
         # parallel execution import
         sqoopImportCommand = '''
         %s %s --target-dir %s/%s/%s --table %s -m 1 &
         ''' % (sqoop_import_params, sqoop_jdbc_params, dw_parent_dir, tblName, biz_date, tblName.upper())
         # parallel execution import
         subprocess.call(sqoopImportCommand, shell=True)
         # cur_time=date "+%F %T"
         # cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                             filename='%s/log/%s_full_imp.log' % (workhome, biz_fmt_date),
                             # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志; a是追加模式，默认如果不写的话，就是追加模式
                             filemode='a',
                             # 日志格式
                             format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
         # logging.info(cur_time + ' : ' + sqoopImportCommand)
         logging.info(sqoopImportCommand)
         time.sleep(15)
   
   ```




  - 注意：
  
    - 如果执行过程中发现Oracle崩溃，可以让每个sqoop命令执行后sleep一段时间。
    - python脚本服务器执行时，删除中文注释
    
    > 在windows下编写多行文件，上传到linux上执行时，会有换行符号文件，如果遇到此类报错，使用命令替换：sed -i 's/\r//g' full_import_tables.txt

4. 执行脚本测试
  
   `/opt/sqoop/one_make/full_import_tables.sh` 或

  `/opt/sqoop/one_make/full_import_tables.py`

5. 查看结果
  
   - 耐心等待，sqoop将不断地往YARN上提交作业，将表中的数据一个个导出。观察scheduler，我们发现现在YARN可以同时调度3-4个JOB同时执行。（我docker宿主机是12G内存）
   
     ![image-20210211000630331](https://s2.loli.net/2022/05/19/WD8apToOsK5G1dY.png)
   
   - 在YARN上查看每个作业的运行情况
   
       - 1. 点击某个JOB，点击Tracking URL旁边的History链接
       
            ![image-20210211000747096](https://s2.loli.net/2022/05/19/ua37w6KB8qCMxeI.png)
       
         2. 点击左侧的Counters，再查看Map-Reduce Framework组中的Map output records就可以知道成功导入到HDFS的行数了。 ![image-20210211000811129](https://s2.loli.net/2022/05/19/kYhzJrQxLvFIRwa.png)
       
         
          - 如果出现故障，可以使用以下方式来kill所有任务
         
            - 先用yarn application -list命令获取当前运行的所有命令
         
            - 再用yarn application -kill命令杀掉所有的MapReduce任务
         
              ```shell
                yarn application -kill application_1607510702808_0025
                yarn application -kill application_1607510702808_0026
                yarn application -kill application_1607510702808_0027
                yarn application -kill application_1607510702808_0028
                yarn application -kill application_1607510702808_0029
              ```

​                