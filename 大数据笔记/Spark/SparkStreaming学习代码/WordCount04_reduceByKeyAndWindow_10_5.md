~~~Scala

import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * 每隔5s计算前10s的数据
 */
object WordCount04_reduceByKeyAndWindow_10_5 {
  def main(args: Array[String]): Unit = {
    //TODO 准备环境
    val conf: SparkConf = new SparkConf().setAppName("WordCount").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val ssc = new StreamingContext(sc, Seconds(5))//每隔5s划分一个批次
    //TODO 1.加载数据
    val lines: ReceiverInputDStream[String] = ssc.socketTextStream("node1", 9999)
    //TODO 2.处理数据
    //第一个参数是函数，第二个参数计算多长的时间的数据：窗口大小，第三个参数是滑动的时间：表示多长时间计算一次（滑动距离）
    //第三个参数必须是上面StreamingContext时间是倍数
    val resultDS = lines.flatMap(_.split(" ")).map((_, 1)).reduceByKeyAndWindow((a: Int, b: Int)=>{a+b},Seconds(10),Seconds(5))
    //TODO 3.输出结果
    resultDS.print()
    //TODO 4.启动并等待结束
    ssc.start()
    ssc.awaitTermination()//注意：流式应用
    //TODO 5.关闭连接
    ssc.stop(stopSparkContext = true,stopGracefully = true)
  }

}

~~~

