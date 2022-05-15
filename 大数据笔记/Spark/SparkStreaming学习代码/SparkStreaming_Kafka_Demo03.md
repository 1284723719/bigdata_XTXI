~~~Scala

import java.sql.{Connection, DriverManager, PreparedStatement, ResultSet}

import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.TopicPartition
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.dstream.InputDStream
import org.apache.spark.streaming.kafka010._
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.mutable

/**
 * 使用kafka,手动提交offset,手动提交到MySQL
 */
object SparkStreaming_Kafka_Demo03 {
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
      //            "auto.commit,interval.ms" -> "1000", //自动提交的时间间隔
      "enable.auto.commit" -> (false: java.lang.Boolean) //是否自动提交offset
    )

    val topics: Array[String] = Array("spark_kafka") //订阅的主题
    //map[主题分区，offset]
    val offsetMap: mutable.Map[TopicPartition, Long] = OffsetUtil.getOffsetMap("sparkdemo", "spark_kafka")
    val stream: InputDStream[ConsumerRecord[String, String]] = if (offsetMap.size > 0) {
      println("MySQL中存储了该消费者组消费该主题的偏移量了记录，接下来从记录处开启消费")
      KafkaUtils.createDirectStream[String, String](
        ssc,
        LocationStrategies.PreferConsistent,
        ConsumerStrategies.Subscribe[String, String](topics, kafkaParams, offsetMap)) //消费策略
    } else {
      println("MySQL中没有存储该消费者组消费该主题的偏移量记录，接下来从latest开始消费")
      KafkaUtils.createDirectStream[String, String](
        ssc,
        LocationStrategies.PreferConsistent,
        ConsumerStrategies.Subscribe[String, String](topics, kafkaParams) //消费策略
      )
    }


    stream.foreachRDD(rdd => {
      //TODO 2.处理数据
      if (!rdd.isEmpty()) {
        rdd.foreach(t => {
          val topic: String = t.topic()
          val partition: Int = t.partition()
          val offset: Long = t.offset()
          val key: String = t.key()
          val value: String = t.value()
          val info = s"topic:${topic},partition:${partition},offset:${offset},key:${key},value:${value}"
          println("消费到的消息为：" + info)

        })
        //获取rdd中offset相关的信息offsetRanges：里面就包含了该批次各个分区的offset信息
        val offsetRanges: Array[OffsetRange] = rdd.asInstanceOf[HasOffsetRanges].offsetRanges
        //提交
        // some time later, after outputs have completed
        //        stream.asInstanceOf[CanCommitOffsets].commitAsync(offsetRanges)
        //手动提交到MySQL
        OffsetUtil.saveOFfsetRange("sparkdemo", offsetRanges)
        println("当前批次的数据已消费并手动提交到MySQL")
      }
    })

    //以批次提交offset


    //TODO 3.输出结果

    //TODO 4.启动并等待结束
    ssc.start()
    ssc.awaitTermination() //注意：流式应用
    //TODO 5.关闭连接
    ssc.stop(stopSparkContext = true, stopGracefully = true)
  }


  object OffsetUtil {
    //
    def saveOFfsetRange(groupid: String, offsetRange: Array[OffsetRange]) = {
      val connection: Connection = DriverManager.getConnection("jdbc:mysql://node1:3306/bigdata1?characterEncoding=UTF-8", "root", "123456")
      //replace into 表示之前有就替换，没有就插入
      val sql: PreparedStatement = connection.prepareStatement("replace into t_offset(`topic`,`partition`,`groupid`,`offset`) values (?,?,?,?)")
      for (o <- offsetRange) {
        sql.setString(1, o.topic)
        sql.setInt(2, o.partition)
        sql.setString(3, groupid)
        sql.setLong(4, o.untilOffset)//untilOffset消费到哪里了
        sql.executeUpdate()
      }
      sql.close()
      connection.close()
    }

    //从数据库读取偏移量map（主题分区，offset）
    def getOffsetMap(groupid: String, topic: String) = {
      val connection: Connection = DriverManager.getConnection("jdbc:mysql://node1:3306/bigdata1?characterEncoding=UTF-8", "root", "123456")
      val sql: PreparedStatement = connection.prepareStatement("select * from t_offset where groupid=? and topic=?")
      sql.setString(1, groupid)
      sql.setString(2, topic)
      val rs: ResultSet = sql.executeQuery()
      val offsetMap: mutable.Map[TopicPartition, Long] = mutable.Map[TopicPartition, Long]()
      while (rs.next()) {
        offsetMap += new TopicPartition(rs.getString("topic"), rs.getInt("partition")) -> rs.getLong("offset")
      }

      rs.close()
      sql.close()
      connection.close()
      offsetMap

    }
  }

}

~~~

