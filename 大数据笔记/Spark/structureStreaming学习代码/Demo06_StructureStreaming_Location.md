~~~Scala
package bigdata.spark.structureStreaming

import org.apache.spark.sql.streaming.StreamingQuery
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}

/**
 *
 * 模拟百度热搜排行榜每隔10s计算最近20s的热搜词
 * 使用自定义输出将结果输出到控制台/HDFS/MySQL
 */
object Demo06_StructureStreaming_Location {
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
    val wordsDS: Dataset[String] = df.as[String].flatMap((_: String).split(" "))
    val result: Dataset[Row] = wordsDS.groupBy('value).count().orderBy('count.desc)


    //TODO 3.输出结果
    //TODO 4.启动并等待结束
    val query: StreamingQuery = result.writeStream
      .format("memory")
      .queryName("t_result")
      .outputMode("complete") //完整模式：表示输出所有数据；必须有聚合才可以用 比如group by 后进行count sum等
      .start()

    while (true) {
      spark.sql("select * from t_result").show()
      Thread.sleep(2000)
    }


//    query.awaitTermination() //注意：后面还有代码要执行，所以这里要注释掉


    //TODO 5.关闭连接
    spark.stop()
  }

}

~~~

