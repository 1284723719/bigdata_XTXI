~~~Scala
package bigdata.spark.structureStreaming


import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.functions._

/**
 *
 * 模拟百度热搜排行榜每隔10s计算最近20s的热搜词
 * 使用自定义输出将结果输出到控制台/HDFS/MySQL
 */
object Demo01_StructureStreaming_Socket {
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
    val df: DataFrame = spark.readStream.format("socket").option("host", "node1").option("port", 9999).load()
    df.printSchema()
//    df.show()

    val result: Dataset[Row] = df.as[String].flatMap((_: String).split(" ")).groupBy('value).count().orderBy('count.desc)

    //TODO 3.输出结果
    result.writeStream
      .format("console")
      .outputMode("complete")
      .start()
        .awaitTermination()

    //TODO 4.启动并等待结束

    //TODO 5.关闭连接
    spark.stop()
  }

}

~~~

