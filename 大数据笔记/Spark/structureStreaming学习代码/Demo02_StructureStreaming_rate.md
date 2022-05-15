~~~Scala
package bigdata.spark.structureStreaming

import org.apache.spark.sql.{DataFrame , SparkSession}
import org.apache.spark.{SparkConf, SparkContext}

/**
 *
 * 模拟百度热搜排行榜每隔10s计算最近20s的热搜词
 * 使用自定义输出将结果输出到控制台/HDFS/MySQL
 */
object Demo02_StructureStreaming_rate {
  def main(args: Array[String]): Unit = {
    System.setProperty("HADOOP_USER_NAME", "root")
    //TODO 准备环境
    val sparkConf: SparkConf = new SparkConf().setMaster("local[*]").setAppName("sparksql")
    val spark: SparkSession = SparkSession.builder().config(sparkConf).config("spark.sql.shuffle.partitions", "4").getOrCreate()
    val sc: SparkContext = spark.sparkContext
    //TODO 1.加载数据
    sc.setLogLevel("WARN")
    import spark.implicits._
    //TODO 2.处理数据
    val result: DataFrame = spark.readStream.format("rate")
      .option("rowsPerSecond", "10") //每s生成的条数
      .option("rampUpTime", "0s") //每条数据生成的间隔时间
      .option("numPartitions", "2") //分区数目
      .load()

    //    df.show()


    //TODO 3.输出结果
    result.writeStream
      .format("console")
      .outputMode("append")
      .option("truncate",false)//表示对列不进行截断，也就是对列内容全部展示
      .start()
      .awaitTermination()

    //TODO 4.启动并等待结束

    //TODO 5.关闭连接
    spark.stop()
  }

}

~~~

