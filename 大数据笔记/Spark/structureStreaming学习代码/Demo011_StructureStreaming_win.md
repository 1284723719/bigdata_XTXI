~~~Scala
package bigdata.spark.structureStreaming

import java.sql.Timestamp

import org.apache.commons.lang3.StringUtils
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.{OutputMode, Trigger}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * 基于事件时间的窗口计算+水印解决数据延迟到达（能够容忍一定程度上的延迟，迟到严重的会被丢弃）
 */
object Demo011_StructureStreaming_win {
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
    val wordDF: DataFrame = df.as[String].filter(StringUtils.isNotBlank(_)).map(line => {
      val arr: Array[String] = line.trim.split(",")
      val timestampStr: String = arr(0)
      val wordsStr: String = arr(1)
      (Timestamp.valueOf(timestampStr), wordsStr)
    }).toDF("timestamp", "word")

    val result: DataFrame = wordDF
      //指定事件时间哪一列，指定时间阈值
      .withWatermark("timestamp", "10 seconds")
      //win定义事件时间是哪一列，窗口长度，滑动间隔
      .groupBy(
        window($"timestamp", "10 seconds", "5 seconds"), $"word"
      ).count()

    //TODO 3.输出结果
    result.writeStream
      .outputMode(OutputMode.Update())
      .format("console")
      .option("truncate", false)
      .trigger(Trigger.ProcessingTime("5 seconds"))
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

