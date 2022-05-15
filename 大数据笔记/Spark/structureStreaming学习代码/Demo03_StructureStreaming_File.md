~~~Scala
package bigdata.spark.structureStreaming

import org.apache.spark.sql.types.{StringType, StructType}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}

/**
 *
 * 模拟百度热搜排行榜每隔10s计算最近20s的热搜词
 * 使用自定义输出将结果输出到控制台/HDFS/MySQL
 */
object Demo03_StructureStreaming_File {
  def main(args: Array[String]): Unit = {
    System.setProperty("HADOOP_USER_NAME", "root")
    //TODO 准备环境
    val sparkConf: SparkConf = new SparkConf().setMaster("local[*]").setAppName("sparksql")
    val spark: SparkSession = SparkSession.builder().config(sparkConf).config("spark.sql.shuffle.partitions", "4").getOrCreate()
    val sc: SparkContext = spark.sparkContext
    //TODO 1.加载数据
    sc.setLogLevel("WARN")
    import spark.implicits._

    val csvSchema: StructType = new StructType()
      .add("id", StringType, nullable = true)
      .add("name", StringType, nullable = true)
      .add("age", StringType, nullable = true)
    //TODO 2.处理数据
    val result: DataFrame = spark.readStream.format("csv").option("sep", ";").option("header", "false")
      .schema(csvSchema) //注意：流式处理对于结构化数据哪怕是有约束也需要单独指定
      .load("D:\\tongbu\\Scala_xtxi\\datas\\input")


    //    df.show()


    //TODO 3.输出结果
    result.writeStream
      .format("console")
      .outputMode("append")
      .option("truncate",false)
      .start()
      .awaitTermination()

    //TODO 4.启动并等待结束

    //TODO 5.关闭连接
    spark.stop()
  }


}

~~~

