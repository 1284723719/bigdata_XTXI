# Avro格式和sqoop导入数据使用avro格式说明文档

## Avro格式介绍

- Avro提供的属性：
  - 1.丰富的数据结构
  - 2.使用快速的压缩二进制数据格式
  - 3.提供容器文件用于持久化数据
  - 4.远程过程调用RPC
  - 5.简单的动态语言结合功能，Avro 和动态语言结合后，读写数据文件和使用 RPC 协议都不需要生成代码，而代码生成作为一种可选的优化只值得在静态类型语言中实现。

- Avro的Schema用json表示，定义了简单数据类型和复杂数据类型

  - 基本类型名称的集合是：
    - null：无值
    - 布尔值：二进制值
    - int：32位有符号整数
    - long：64位有符号整数
    - float：单精度（32位）IEEE 754浮点数
    - double：双精度（64位）IEEE 754浮点数
    - bytes：8位无符号字节序列
    - string：Unicode字符序列

  > 基本类型没有指定的属性，基本类型名称也是定义的类型名称。因此，例如，shema“string”等效于：{“ type”：“string”}

- 复杂数据类型
  
- Avro支持六种复杂类型：记录，枚举，数组，映射，联合和固定类型。
  
- 以工单表为例，表的schema信息(部分字段)，avro格式为:

  ```json
  {
    "type" : "record",
    "name" : "CISS4_CISS_SERVICE_WORKORDER",
    "doc" : "派工单",
    "fields" : [ {
      "name" : "ID",
      "type" : [ "null", "string" ],
      "default" : null,
      "columnName" : "ID",
      "sqlType" : "12",
      "doc" : "派工单ID"
    }, {
      "name" : "CALLACCEPT_ID",
      "type" : [ "null", "string" ],
      "default" : null,
      "columnName" : "CALLACCEPT_ID",
      "sqlType" : "12",
      "doc" : "来电受理单id"
    }, {
      "name" : "GPRS_DISTANCE_1_VAL",
      "type" : [ "null", "string" ],
      "default" : null,
      "columnName" : "GPRS_DISTANCE_1_VAL",
      "sqlType" : "12",
      "doc" : "gprs出发-离站距离（公里）"
    }, {
      "name" : "GPRS_DISTANCE_2_VAL",
      "type" : [ "null", "string" ],
      "default" : null,
      "columnName" : "GPRS_DISTANCE_2_VAL",
      "sqlType" : "12",
      "doc" : "gprs离站-完工距离（公里）"
    } ],
    "tableName" : "CISS4.CISS_SERVICE_WORKORDER"
  }
  ```

## sqoop使用avro格式导入数据

1. 上传表对应的avsc文件，文件在sqoop的home目录下，java_code目录中

   ![img](https://s2.loli.net/2022/05/19/VaPrgjFBWD2nXGl.jpg) 

2.  以ciss_service_workorder为例，CISS4_CISS_SERVICE_WORKORDER.avsc文件到hdfs上

- 上传到hdfs的/data/dw/ods/avsc目录下
  
3. 创建avro格式的工单表

   (1) hive引擎

   ```sql
   create external table if not exists one_make_ods.ciss_service_workorder comment '派工单'partitioned by (dt string)row format serde 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'stored as avro location '/data/dw/ods/one_make/incr_imp/ciss4.ciss_service_workorder'TBLPROPERTIES ('avro.schema.url'='hdfs:///data/dw/ods/avsc/CISS4_CISS_SERVICE_WORKORDER.avsc');
   ```

   (2) sparksql引擎

   ```sql
   create external table if not exists one_make_ods.ciss_service_workorder comment '派工单'partitioned by (dt string)row format serde 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'stored as inputformat 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'  OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'location '/data/dw/ods/one_make/incr_imp/ciss4.ciss_service_workorder'TBLPROPERTIES ('avro.schema.url'='hdfs:///data/dw/ods/avsc/CISS4_CISS_SERVICE_WORKORDER.avsc');
   ```

4. 查看建表情况

   `show create table one_make_ods.ciss_service_workorder;`

5. 导入分区数据到工单表

   ```sql
   alter table one_make_ods.ciss_service_workorder add if not exists partition (dt='20210101') location '/data/dw/ods/one_make/incr_imp/ciss4.ciss_service_workorder/20210101'
   ```

