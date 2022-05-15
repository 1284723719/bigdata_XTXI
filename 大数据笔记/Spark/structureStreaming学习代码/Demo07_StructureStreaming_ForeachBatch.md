~~~Scala
package bigdata.spark.structureStreaming

import org.apache.spark.sql.{DataFrame, Dataset, Row, SaveMode, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}

/**
 *
 * 模拟百度热搜排行榜每隔10s计算最近20s的热搜词
 * 使用自定义输出将结果输出到控制台/HDFS/MySQL
 */
object Demo07_StructureStreaming_ForeachBatch {
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
    val ds: Dataset[String] = df.as[String]
    val wordsDS: Dataset[String] = ds.flatMap((_: String).split(" "))
    val result: Dataset[Row] = wordsDS.groupBy('value).count().orderBy('count.desc)


    //TODO 3.输出结果
    //TODO 4.启动并等待结束
    result.writeStream.foreachBatch((ds: Dataset[Row], batchId: Long) => {
      //自定义输出到控制台
      println("===============")
      println(s"batchID:${batchId}")
      println("===============")
      ds.show()
      //自定义输出MySQL
      ds.write.format("jdbc")
        .mode(SaveMode.Overwrite)
        //.option("driver","com.mysql.cj.jdbc.Driver")mysql8.0
        //.option("url","jdbc:mysql://node1:3306/?serverTimezone=UTC&characterEncoding=utf8&useUnicode=true")//mysql8.0
        .option("url", "jdbc:mysql://node1:3306/bigdata1")
        .option("dbtable", "t_struct_words")//会自动创建
        .option("user", "root")
        .option("password", "123456")
        .save()
    }).outputMode("complete").start().awaitTermination()


    //TODO 5.关闭连接
    spark.stop()
  }

}

~~~

