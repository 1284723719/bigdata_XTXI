~~~Scala
package bigdata.spark.StreamingHwma

import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * 批次实现累加
 */

object WordCount02_updateStateByKey {
  def main(args: Array[String]): Unit = {
    System.setProperty("HADOOP_USER_NAME", "root")
    //TODO 准备环境
    val conf: SparkConf = new SparkConf().setAppName("WordCount").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val ssc = new StreamingContext(sc, Seconds(5)) //每隔5s划分一个批次
    //注意：state存在checkpoint中
    ssc.checkpoint("file:\\D:\\tongbu\\Scala_xtxi\\cp")
    //TODO 1.加载数据
    val lines: ReceiverInputDStream[String] = ssc.socketTextStream("node1", 9999)
    //TODO 2.处理数据
    //定义一个函数用来处理状态：把当前数据和历史状态进行累加
    //currentValue:表示该key的当前批次的值：如[1,1]
    //historyValue表示该key的历史值，第一次是0，后面就是之前的累加值如1
    val updateFunc=(currentValues:Seq[Int],historyValue:Option[Int])=>{
      if(currentValues.size>0){
        val currentResult: Int = currentValues.sum + historyValue.getOrElse(0)
      Some(currentResult)
      }else{
        historyValue
      }

    }
    val resultDS: DStream[(String, Int)] = lines.flatMap(_.split(" ")).map((_, 1)).updateStateByKey(updateFunc)
    //TODO 3.输出结果
    resultDS.print()
    //TODO 4.启动并等待结束
    ssc.start()
    ssc.awaitTermination() //注意：流式应用
    //TODO 5.关闭连接
    ssc.stop(stopSparkContext = true, stopGracefully = true)
  }

}

~~~

