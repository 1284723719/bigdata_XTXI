~~~Scala

import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

object WordCount01_socket {
  def main(args: Array[String]): Unit = {
    //TODO 准备环境
    val conf: SparkConf = new SparkConf().setAppName("WordCount").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val ssc = new StreamingContext(sc, Seconds(5))//每隔5s划分一个批次
    //TODO 1.加载数据
    val lines: ReceiverInputDStream[String] = ssc.socketTextStream("node1", 9999)
    //TODO 2.处理数据
    val resultDS: DStream[(String, Int)] = lines.flatMap(_.split(" ")).map((_, 1)).reduceByKey(_ + _)
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

