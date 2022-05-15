~~~Scala
package bigdata.spark.StreamingHwma


import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.dstream.{DStream, InputDStream}
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, KafkaUtils, LocationStrategies}
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
 * 使用kafka
 */
object SparkStreaming_Kafka_Demo01 {
  def main(args: Array[String]): Unit = {
    //TODO 准备环境
    val conf: SparkConf = new SparkConf().setAppName("WordCount").setMaster("local[*]")
    val sc = new SparkContext(conf)
    val ssc = new StreamingContext(sc, Seconds(5)) //每隔5s划分一个批次
    //TODO 1.加载数据

    val kafkaParams: Map[String, Object] = Map[String, Object](
      "bootstrap.servers" -> "node1:9092", //集群地址
      "key.deserializer" -> classOf[StringDeserializer], //key反序列化
      "value.deserializer" -> classOf[StringDeserializer], //vlaue反序列化
      "group.id" -> "sparkdemo", //消费者组
      //earliest:表示如果有offset记录从offset记录开始消费，如果没有从最早的消息开始消费
      //latest：表示如果有offset记录中offset记录开启消费，如果没有从最后/最新的消息开始消费
      //none：表示如果有offset记录从offset记录开始消费，如果没有就报错
      "auto.offset.reset" -> "latest",
      "auto.commit,interval.ms" -> "1000", //自动提交的时间间隔
      "enable.auto.commit" -> (true: java.lang.Boolean) //是否自动提交offset
    )

    val topics: Array[String] = Array("spark_kafka") //订阅的主题
    val stream: InputDStream[ConsumerRecord[String, String]] = KafkaUtils.createDirectStream[String, String](
      ssc,
      LocationStrategies.PreferConsistent,
      ConsumerStrategies.Subscribe[String, String](topics, kafkaParams) //消费策略
    )

    //TODO 2.处理数据
    val info: DStream[String] = stream.map(t => {
      val topic: String = t.topic()
      val partition: Int = t.partition()
      val offset: Long = t.offset()
      val key: String = t.key()
      val value: String = t.value()
      val info = s"topic:${topic},partition:${partition},offset:${offset},key:${key},value:${value}"
      info
    })

    //TODO 3.输出结果
    info.print()

    //TODO 4.启动并等待结束
    ssc.start()
    ssc.awaitTermination() //注意：流式应用
    //TODO 5.关闭连接
    ssc.stop(stopSparkContext = true, stopGracefully = true)
  }

}

~~~

