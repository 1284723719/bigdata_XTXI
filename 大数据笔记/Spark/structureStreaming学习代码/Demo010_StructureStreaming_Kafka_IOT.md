~~~Scala
package bigdata.spark.structureStreaming

import org.apache.commons.lang3.StringUtils
import org.apache.spark.sql.{DataFrame, Dataset, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.DoubleType

/**
 * 整合kafka从stationTopic消费数据-->使用structureStreaming进行ETL-->将结果写道控制台
 * iotTopic --->StructuredStreaming-->控制台
 */
object Demo010_StructureStreaming_Kafka_IOT {
  def main(args: Array[String]): Unit = {
    System.setProperty("HADOOP_USER_NAME", "root")
    //TODO 准备环境
    val sparkConf: SparkConf = new SparkConf().setMaster("local[*]").setAppName("sparksql")
    val spark: SparkSession = SparkSession.builder().config(sparkConf).config("spark.sql.shuffle.partitions", "4").getOrCreate()
    val sc: SparkContext = spark.sparkContext
    sc.setLogLevel("WARN")
    import spark.implicits._

    //TODO 1.加载数据-kafka-iotTopic
    val kafkaDF: DataFrame = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "192.168.88.161:9092")
      .option("subscribe", "iotTopic")
      .load()


    val valueDS: Dataset[String] = kafkaDF.selectExpr("CAST(value as STRING)").as[String]


    //TODO 2.处理数据-ETL
    //需求：统计信号强度>30的各种设备类型对应的数量和平均信号强度
    //解析json（也就是增加schema：字段名和类型)
    //    方式1：fostJson/Gson 工具包
    //方式2：使用sparkSQL内置函数
    val schemaDF: DataFrame = valueDS.filter(StringUtils.isNoneBlank(_)) //过滤不为空的数据
      .select(
        get_json_object($"value", "$.device").as("device_id"),
        get_json_object($"value", "$.deviceType").as("deviceType"),
        get_json_object($"value", "$.signal").cast(DoubleType).as("signal")
      )
    //     sql
    schemaDF.createOrReplaceTempView("t_iot")
    val sql: String =
      """
        |select deviceType,count(*) as counts ,avg(signal) as avgsignal
        |from t_iot
        |where signal > 30
        |group by deviceType
        |""".stripMargin
    val result1: DataFrame = spark.sql(sql)

    //dsl
    val result2: DataFrame = schemaDF.where('signal > 30).groupBy('deviceType).agg(count('device_id).as("counts"), avg('signal).as("avgsignal"))

    //TODO 3.输出结果
    result1.writeStream
      .format("console")
      .outputMode("complete")
//      .option("truncate", false)
      .start()

    result2.writeStream
      .format("console")
      .outputMode("complete")
      //      .trigger(Trigger.ProcessingTime(0))
      .start()
      .awaitTermination()

    //TODO 4.启动并等待结束



    //TODO 5.关闭连接
    spark.stop()
  }

}

//0.kafka准备好
//1.启动数据模拟程序
//3.启动本个程序

~~~

