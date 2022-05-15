~~~Scala
package bigdata.spark.structureStreaming

import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}

/**
 *
 * 模拟百度热搜排行榜每隔10s计算最近20s的热搜词
 * 使用自定义输出将结果输出到控制台/HDFS/MySQL
 */
object Demo05_StructureStreaming_outputMode {
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

    wordsDS.createOrReplaceTempView("t_words")
    val sql =
      """
        |select value,count(*) as counts from t_words
        |group by value
        |order by counts desc
        |""".stripMargin
    val result2: DataFrame = spark.sql(sql)






    //TODO 3.输出结果
    //TODO 4.启动并等待结束
    result.writeStream
      .format("console")
      .outputMode("complete")//完整模式：表示输出所有数据；必须有聚合才可以用 比如group by 后进行count sum等
//      .outputMode("append")//追加模式/默认模式，表示只输出新增的数据，只支持简单查询 比如：就spilt直接输出，或者读取文件
//      .outputMode("update")//更新模式：表示指数出租变化的/有更新的数据，不支持排序 比如group后直接输出使用
      .start()
//      .awaitTermination()//注意：后面还有代码要执行，所以这里要注释掉

    result2.writeStream
      .format("console")
      .outputMode("complete")
      .start()
      .awaitTermination()




    //TODO 5.关闭连接
    spark.stop()
  }

}

~~~

