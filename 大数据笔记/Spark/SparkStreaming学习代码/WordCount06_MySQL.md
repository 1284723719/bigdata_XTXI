~~~Scala

import java.sql.{Connection, DriverManager, PreparedStatement, Timestamp}

import org.apache.spark.rdd.RDD
import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
 *
 * 模拟百度热搜排行榜每隔10s计算最近20s的热搜词
 * 使用自定义输出将结果输出到控制台/HDFS/MySQL
 */
object WordCount06_MySQL {
  def main(args: Array[String]): Unit = {
    //TODO 准备环境
    val conf: SparkConf = new SparkConf().setAppName("WordCount").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val ssc = new StreamingContext(sc, Seconds(5)) //每隔5s划分一个批次
    //TODO 1.加载数据
    val lines: ReceiverInputDStream[String] = ssc.socketTextStream("node1", 9999)
    //TODO 2.处理数据
    //第一个参数是函数，第二个参数计算多长的时间的数据：窗口大小，第三个参数是滑动的时间：表示多长时间计算一次（滑动距离）
    //第三个参数必须是上面StreamingContext时间是倍数
    //注意DStream没有提供直接排序的方法，所以需要直接对底层的RDD操作
    val resultDS: DStream[(String, Int)] = lines.flatMap(_.split(" ")).map((_, 1)).reduceByKeyAndWindow((a: Int, b: Int) => {
      a + b
    }, Seconds(20), Seconds(10))
    //表示对DStream底层的RDD进行草哦组并返回结果
    val sortResultDS: DStream[(String, Int)] = resultDS.transform(rdd => {
      val sortRDD: RDD[(String, Int)] = rdd.sortBy(_._2, false)
      val top3: Array[(String, Int)] = sortRDD.take(3)
      top3.foreach(println)
      sortRDD
    })
    //TODO 3.输出结果
    sortResultDS.print()
    //自定义输出
    sortResultDS.foreachRDD((rdd,time)=>{
      val milliseconds: Long = time.milliseconds
      rdd.foreach(println)
      rdd.coalesce(1).saveAsTextFile("file:\\D:\\tongbu\\Scala_xtxi\\output\\result-"+milliseconds)
      //输出MySQL
      rdd.foreachPartition(t=>{
        //开启连接
        val conn: Connection = DriverManager.getConnection("jdbc:mysql://node1:3306/hive3?createDatabaseIfNotExist=true&amp;useSSL=false", "root", "123456")
        val sql="insert into table 表名 vlaues (?,?,?)"
        val ps: PreparedStatement = conn.prepareStatement(sql)
        t.foreach(t=>{
          val word: String = t._1
          val count: Int = t._2
          ps.setTimestamp(1,new Timestamp(milliseconds))
          ps.setString(2,word)
          ps.setInt(3,count)
          ps.addBatch()
        })
        ps.executeBatch()
        //关闭连接
        if(conn != null)conn.close()
        if(ps != null)ps.close()
      })
    })

    //TODO 4.启动并等待结束
    ssc.start()
    ssc.awaitTermination() //注意：流式应用
    //TODO 5.关闭连接
    ssc.stop(stopSparkContext = true, stopGracefully = true)
  }

}

~~~

