~~~Scala
package bigdata.spark.structureStreaming


import org.apache.commons.lang3.StringUtils
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.OutputMode
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * 基于事件时间的窗口计算+水印解决数据延迟到达（能够容忍一定程度上的延迟，迟到严重的会被丢弃）
 */
object Demo012_StructureStreaming_Deduplication {
  def main(args: Array[String]): Unit = {
    System.setProperty("HADOOP_USER_NAME", "root")
    //TODO 准备环境
    val sparkConf: SparkConf = new SparkConf().setMaster("local[*]").setAppName("sparksql")
    val spark: SparkSession = SparkSession.builder().config(sparkConf).config("spark.sql.shuffle.partitions", "4").getOrCreate()
    val sc: SparkContext = spark.sparkContext
    sc.setLogLevel("WARN")
    import spark.implicits._

    //TODO 1.加载数据socket
    val df: DataFrame = spark.readStream.format("socket").option("host", "node1").option("port", 9999).load()


    //TODO 2.处理数据-ETL
    //{"eventTime": "2016-01-10 10:01:50","eventType": "browse","userID":"1"}
    val wordDF: DataFrame = df.as[String].filter(StringUtils.isNotBlank(_)).select(
      get_json_object($"value", "$.eventTime").as("eventTime"),
      get_json_object($"value", "$.eventType").as("eventType"),
      get_json_object($"value", "$.userID").as("userID")
    )
    val result: Dataset[Row] = wordDF.dropDuplicates("userID", "eventType", "eventTime")
    val count: DataFrame = result.groupBy("userID").count()
    println("count")


    //TODO 3.输出结果
    count.writeStream
      .outputMode(OutputMode.Complete())
      .format("console")
      .option("truncate", false)
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

