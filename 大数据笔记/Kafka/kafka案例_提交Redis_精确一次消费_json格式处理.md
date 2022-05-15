~~~Scala
// Kafka提交到Redis（可以替换MySQL），精确一次消费，将json数据转换为json格式，然后经过处理转换为json格式发送给kafka
package com.atguigu.gmall.realtime.app

import java.lang

import com.alibaba.fastjson.serializer.SerializeConfig
import com.alibaba.fastjson.{JSON, JSONArray, JSONObject}
import com.atguigu.gmall.realtime.bean.{PageActionLog, PageDisplayLog, PageLog, StartLog}
import com.atguigu.gmall.realtime.util.{MyKafkaUtils, MyOffsetUtils}
import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.TopicPartition
import org.apache.spark.rdd.RDD
import org.apache.spark.streaming.dstream.{DStream, InputDStream}
import org.apache.spark.streaming.kafka010.{HasOffsetRanges, OffsetRange}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
 * 日志数据的消费分流
 * 1.准备实时处理环境streamingContext
 * 2.从kafka中消费数据
 * 3.处理数据
 *  3.1转换数据结构
 * 专用结构 Bean
 * 通用结构 Map JsonObject
 *  3.2分流
 * 4.写出到DWD层
 */
object Ods_BaseLogApp {
  def main(args: Array[String]): Unit = {
    //准备实时环境
    //TODO 注意并行度与kafka中topic的分区个数的对应关系
    val conf: SparkConf = new SparkConf().setAppName("ods_base_log_app").setMaster("local[3]")
    val sc = new SparkContext(conf)
    val ssc = new StreamingContext(sc, Seconds(5))

    //2.从kafka中消费数据
    val topicName: String = "ODS_BASE_LOG_1018" //对应生成器配置中的主题名
    val groupId: String = "ODS_BASES_LOG_GROUP_1018"

    //TODO 从Redis中读取offset，指定offset进行消费
    //想一想一定能获取到数据吗，需要先让kafka自己消费一次
    val offsets: Map[TopicPartition, Long] = MyOffsetUtils.readOffset(topicName, groupId)

    var KafkaDStream: InputDStream[ConsumerRecord[String, String]] = null
    if(offsets != null && offsets.nonEmpty){
      //指定offset进行消费
      KafkaDStream= MyKafkaUtils.getKafkaDStream(ssc, topicName, groupId,offsets)

    }else{
      //默认offset进行消费
      KafkaDStream= MyKafkaUtils.getKafkaDStream(ssc, topicName, groupId)
    }


    //TODO 补充：从当前消费到的数据中提取offset,不对流中的数据做任何处理
    var offsetRanges: Array[OffsetRange] =null
    val offsetRangesDStream: DStream[ConsumerRecord[String, String]] = KafkaDStream.transform(
      (rdd: RDD[ConsumerRecord[String, String]]) => {
        //需要转换,提取offset信息，在Driver端中执行，如果是executor该怎么做，需要想一想
        offsetRanges = rdd.asInstanceOf[HasOffsetRanges].offsetRanges
        //不做操作，把rdd返回回去
        rdd
      }
    )


    //3.处理数据
    //3.1转换数据结构
    val jsonObjDStream: DStream[JSONObject] = offsetRangesDStream.map(
      (consumerRecord: ConsumerRecord[String, String]) => {
        //获取ConsumerRecord中的value，value就是日志数据
        val log: String = consumerRecord.value()
        //转换成json对象
        val jsonObj: JSONObject = JSON.parseObject(log)
        //返回
        jsonObj
      }
    )
    //    jsonObjDStream.print()
    //3.2分流
    //日志数据：
    //页面访问数据：公共字段、页面数据、曝光数据、事件数据、错误数据
    //启动数据：启动数据、公共字段、错误数据

    val DWD_PAGE_LOG_TOPIC: String = "DWD_PAGE_LOG_TOPIC_1018" //页面访问
    val DWD_PAGE_DISPLAY_TOPIC: String = "DWD_PAGE_DISPLAY_TOPIC_1018" //页面曝光
    val DWD_PAGE_ACTION_TOPIC: String = "DWD_PAGE_ACTION_TOPIC_1018" //页面事件
    val DWD_START_LOG_TOPIC: String = "DWD_START_LOG_TOPIC_1018" //启动数据
    val DWD_ERROR_LOG_TOPIC: String = "DWD_ERROR_LOG_TOPIC_1018" //错误数据

    //分流的规则：
    //  错误数据：不做任何拆分，只要包含错误字段，直接整条数据发送到对应的topic
    //  页面数据：拆分成页面访问，曝光，事件 分别发送到对应的topic
    //  启动数据：发送到对应的topic

    jsonObjDStream.foreachRDD(
      rdd => {
        rdd.foreachPartition(
          jsonObjIter=>{
            for (jsonObj <- jsonObjIter) {
              //分流过程
              //分流错误数据
              val errObj: JSONObject = jsonObj.getJSONObject("err")
              if (errObj != null) {
                //将错误数据发送到错误主题,需要将json数据装换,json是阿里的是Java写的，需要传一个值new SerializeConfig(true),不再去找get，set方法（java对象需要一个get，set方法，Scala不用get，set方法）
                MyKafkaUtils.send(DWD_ERROR_LOG_TOPIC, JSON.toJSONString(jsonObj, new SerializeConfig(true)))
              } else {
                //提取公共字段
                val commonObj: JSONObject = jsonObj.getJSONObject("common")
                val ar: String = commonObj.getString("ar")
                val uid: String = commonObj.getString("uid")
                val os: String = commonObj.getString("os")
                val ch: String = commonObj.getString("ch")
                val is_new: String = commonObj.getString("is_new")
                val md: String = commonObj.getString("md")
                val mid: String = commonObj.getString("mid")
                val vc: String = commonObj.getString("vc")
                val ba: String = commonObj.getString("ba")
                //提取时间戳
                val ts: lang.Long = jsonObj.getLong("ts")
                //页面数据
                val pageObj: JSONObject = jsonObj.getJSONObject("page")
                if (pageObj != null) {
                  //提取page字段
                  val page_id: String = pageObj.getString("page_id")
                  val pageItem: String = pageObj.getString("item")
                  val pageType: String = pageObj.getString("item_type")
                  val duringTime: lang.Long = pageObj.getLong("during_time")
                  val last_page_id: String = pageObj.getString("last_page_id")
                  val source_type: String = pageObj.getString("source_type")
                  //封装成pagelog
                  val pageLog: PageLog = PageLog(mid, uid, ar, ch, is_new, md, os, vc, ba, page_id, last_page_id, pageItem, pageType, duringTime, source_type, ts)
                  //发送到页面访问主题,json是阿里的是Java写的，需要传一个值new SerializeConfig(true),不再去找get，set方法（java对象需要一个get，set方法，Scala不用get，set方法）
                  MyKafkaUtils.send(DWD_PAGE_LOG_TOPIC, JSON.toJSONString(pageLog, new SerializeConfig(true)))
                  //提取曝光数据,[{},{}],jsonaerray是java代码 需要自己写for
                  val displaysJsonArr: JSONArray = jsonObj.getJSONArray("displays")
                  if (displaysJsonArr != null && displaysJsonArr.size() > 0) {
                    //循环拿到每个曝光
                    for (i <- 0 until displaysJsonArr.size()) {
                      //提取曝光字段
                      val displayObj: JSONObject = displaysJsonArr.getJSONObject(i)
                      val displayType: String = displayObj.getString("display_type")
                      val displayItem: String = displayObj.getString("item")
                      val displayItemType: String = displayObj.getString("item_type")
                      val PosId: String = displayObj.getString("pos_id")
                      val order: String = displayObj.getString("order")
                      //封装对象
                      val pageDisplayLog: PageDisplayLog = PageDisplayLog(md, uid, ar, ch, is_new, md, os, vc, ba, page_id, last_page_id, pageItem, pageType, duringTime, source_type, displayType, displayItem, displayItemType, order, PosId, ts)
                      MyKafkaUtils.send(DWD_PAGE_DISPLAY_TOPIC, JSON.toJSONString(pageDisplayLog, new SerializeConfig(true)))
                    }
                  }
                  //提取事件数据
                  val actionsArr: JSONArray = jsonObj.getJSONArray("actions")
                  if (actionsArr != null && actionsArr.size() > 0) {
                    for (i <- 0 until actionsArr.size()) {
                      val actionObj: JSONObject = actionsArr.getJSONObject(i)
                      val actionId: String = actionObj.getString("action_id")
                      val actionItem: String = actionObj.getString("item")
                      val actionItemType: String = actionObj.getString("item_type")
                      val actionTs: lang.Long = actionObj.getLong("ts")
                      val actionLog: PageActionLog = PageActionLog(md, uid, ar, ch, is_new, md, os, vc, ba, page_id, last_page_id, pageItem, pageType, duringTime, actionId, actionItem, actionItemType, source_type, actionTs, ts)
                      MyKafkaUtils.send(DWD_PAGE_ACTION_TOPIC, JSON.toJSONString(actionLog, new SerializeConfig(true)))
                    }
                  }
                }
                //启动数据
                val startObj: JSONObject = jsonObj.getJSONObject("start")
                if (startObj != null) {
                  val entry: String = startObj.getString("entry")
                  val open_ad_skip_ms: lang.Long = startObj.getLong("open_ad_skip_ms")
                  val open_ad_ms: lang.Long = startObj.getLong("open_ad_ms")
                  val loading_time: lang.Long = startObj.getLong("loading_time")
                  val open_ad_id: String = startObj.getString("open_ad_id")
                  val startLog: StartLog = StartLog(md, uid, ar, ch, is_new, md, os, vc, ba, entry, open_ad_id, loading_time, open_ad_ms, open_ad_skip_ms, ts)
                  MyKafkaUtils.send(DWD_START_LOG_TOPIC, JSON.toJSONString(startLog, new SerializeConfig(true)))
                }
              }
            }
            //刷写kafka,每批次每分区执行一次
            MyKafkaUtils.flush()
          }
        )

/*        rdd.foreach(
          jsonObj => {
         //foreach里面:executor端执行,如果提交offset则会提交多次，每条数据执行一次
          }

        )*/
        //foreachRDD里面foreach外面: 如果offset提交 Driver 端执行，一批次执行一次（周期性）
        MyOffsetUtils.saveOffset(topicName,groupId,offsetRanges)
      }
    )
    //foreachRDD外面：如果提交offset是在主程序里面，Driver执行，每次启动执行一次

    ssc.start()
    ssc.awaitTermination()
  }
}

/*-----------------------------------------------------------------------------------------------------------------*/

/**
 * 配置类
 */
object MyConfig {
  val KAFKA_BOOTSTRAP_SERVER:String = "kafka.bootstrap-servers"
  val REDIS_HOST:String="redis.host"
  val REDIS_PORT:String="redis.port"
}


/*-----------------------------------------------------------------------------------------------------------------*/
import java.util

import org.apache.kafka.clients.consumer.{ConsumerConfig, ConsumerRecord}
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerConfig, ProducerRecord}
import org.apache.kafka.common.TopicPartition
import org.apache.spark.streaming.StreamingContext
import org.apache.kafka.common.serialization.StringSerializer
import org.apache.spark.streaming.dstream.InputDStream
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, KafkaUtils, LocationStrategies}

import scala.collection.mutable

/**
 * kafka工具类，用于生产数据和消费数据
 */
object MyKafkaUtils {

  /**
   * 消费者配置
   * ConsumerConfig
   */
  private val consumerConfigs: mutable.Map[String, Object] = mutable.Map[String, Object](
    //kafka集群位置
    //    ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG -> "node1:9092,node2:9092,node3:9092",
    ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG -> MyPropsUtils(MyConfig.KAFKA_BOOTSTRAP_SERVER),
    //kv反序列化器
    ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG -> "org.apache.kafka.common.serialization.StringDeserializer",
    ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG -> "org.apache.kafka.common.serialization.StringDeserializer",
    //groupid
    //offset提交 自动 手动
    ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG -> "false",
    //offset自动提交间隔
    //    ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG
    //offset重置
    ConsumerConfig.AUTO_OFFSET_RESET_CONFIG -> "latest"
  )


  /**
   * 基于sparkstreaming消费,获取到kafkaDStream,使用默认的offset
   */

  def getKafkaDStream(ssc: StreamingContext, topic: String, groupId: String): InputDStream[ConsumerRecord[String, String]] = {
    consumerConfigs.put(ConsumerConfig.GROUP_ID_CONFIG, groupId)
    val kafkaDStream: InputDStream[ConsumerRecord[String, String]] = KafkaUtils.createDirectStream(
      ssc,
      LocationStrategies.PreferConsistent,
      ConsumerStrategies.Subscribe[String, String](Array(topic), consumerConfigs))
    kafkaDStream
  }

  /**
   * 基于sparkstreaming消费,获取到kafkaDStream,使用指定的offset
   */

  def getKafkaDStream(ssc: StreamingContext, topic: String, groupId: String,offsets: Map[TopicPartition, Long]): InputDStream[ConsumerRecord[String, String]] = {
    consumerConfigs.put(ConsumerConfig.GROUP_ID_CONFIG, groupId)
    val kafkaDStream: InputDStream[ConsumerRecord[String, String]] = KafkaUtils.createDirectStream(
      ssc,
      LocationStrategies.PreferConsistent,
      ConsumerStrategies.Subscribe[String, String](Array(topic), consumerConfigs))
    kafkaDStream
  }

  /**
   * 生产者对象
   */
  val producer: KafkaProducer[String, String] = createProducer()

  /**
   * 创建生产者对象
   * ProducerConfig
   */
  def createProducer(): KafkaProducer[String, String] = {
    val producerConfigs = new util.HashMap[String, AnyRef]
    //kafka集群位置
    //    producerConfigs.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "node1:9092,node2:9092,node3:9092")
    producerConfigs.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, MyPropsUtils(MyConfig.KAFKA_BOOTSTRAP_SERVER))
    producerConfigs.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer")
    producerConfigs.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer")
    //ack
    producerConfigs.put(ProducerConfig.ACKS_CONFIG, "all")
    //幂等配置,默认为false
    producerConfigs.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true")

    val produce = new KafkaProducer[String, String](producerConfigs)
    produce
  }

  /**
   * 生产(按照默认的黏性分区策略
   */

  def send(topic: String, msg: String): Unit = {
    producer.send(new ProducerRecord[String, String](topic, msg))
  }

  /**
   * 生产（按照key进行分区）
   */

  def send(topic: String, key: String, msg: String): Unit = {
    producer.send(new ProducerRecord[String, String](topic, key, msg))
  }

  /**
   * 关闭生产者对象
   */
  def close():Unit={
    if(producer != null) producer.close()
  }

  /**
   * 刷写，将缓冲区的数据刷写到磁盘
   */
  def flush():Unit={
    producer.flush()
  }
}

/*-----------------------------------------------------------------------------------------------------------------*/
import java.util

import org.apache.kafka.common.TopicPartition
import org.apache.spark.streaming.kafka010.OffsetRange
import redis.clients.jedis.Jedis

import scala.collection.mutable

/**
 * Offset管理工具类，用于往Redis中存储和读取offset
 *
 * 管理方案：
 *  1.后置提交偏移量 -> 手动控制偏移量提交
 *  2.手动控制偏移量提交 -> SparkStreaming提交了手动提交方案，但是我们不能用,因为我们会对DStream的结构进行转换
 *  3.手动的提取偏移量维护到Redis中
 *      -> 从Kafka中消费到数据，先提取偏移量
 *      -> 等数据成功写出后，将偏移量存储到Redis中
 *      -> 从Kafka中消费之前，先到Redis中读取偏移量，使用读取到的偏移量到Kafka中消费数据
 *
 *  4.手动的将偏移量存储到Redis中，每次消费数据需要使用存储的offset进行消费，每次消费数据后，要将本次消费的offset存储到Redis中
 */
object MyOffsetUtils {
  /**
   * 往Redis中存储offset
   * 问题：存的offset从哪来？
   *          从消费到的数据中提取出来的，传入该方法中。
   *          offsetRanges: Array[OffsetRange]
   *      offset的结构是什么？
   *          Kafka中offset维护的结构
   *            groupId + topic + partition => offset
   *          从传入进来的offset中提取关键信息
   *      在Redis中怎么存？
   *          类型： hash
   *          key: groupId + topic
   *          value: partition - offset , partition - offset ...
   *          写入API： hset / hmset
   *          读取API： hgetall
   *          是否过期： 不过期
   */
  def saveOffset(topic:String,groupId:String,offsetRanges: Array[OffsetRange]):Unit={
    if(offsetRanges != null && offsetRanges.length > 0){
      //创建一个map
      val offsets = new util.HashMap[String, String]()
      for (offsetRange <- offsetRanges) {
        //获取分区
        val partition: Int = offsetRange.partition
        //获取结束的offset，有个开始的offset一个结束的offset
        val endOffset: Long = offsetRange.untilOffset
        //封装成map
        offsets.put(partition.toString,endOffset.toString)
      }
      println("提交offset："+offsets)
      //往Redis中存
      val jedis: Jedis = MyRedisUtils.getJedisFromPool()
      val redisKey:String = s"offsets:$topic:$groupId"
      jedis.hset(redisKey,offsets)

      jedis.close()


    }

  }
  /**
   * 从Redis中读取存储的offset
   *
   * 问题：
   *  如何让SparkStreaming通过指定的offset进行消费？
   *   SparkStreaming要求的offset的格式是什么？
   *      Map[TopicPartition,Long]
   */

  def readOffset(topic:String,groupId:String):Map[TopicPartition,Long]={
    val jedis: Jedis = MyRedisUtils.getJedisFromPool()
    val redisKey:String = s"offsets:$topic:$groupId"
    //java 的map
    val offsets: util.Map[String, String] = jedis.hgetAll(redisKey)
    println("读取到offset："+ offsets)
    val results: mutable.Map[TopicPartition, Long] = mutable.Map[TopicPartition, Long]()
    //将Java的map转换成Scala的map进行迭代
    import scala.collection.JavaConverters._
    for ((partition,offset) <- offsets.asScala) {
      val tp = new TopicPartition(topic, partition.toInt)
      results.put(tp,offset.toLong)
    }
    jedis.close()
    //把可变的转换成不可变的Map
    results.toMap
  }
}

/*-----------------------------------------------------------------------------------------------------------------*/
import java.util.ResourceBundle

/**
 * 配置文件解析类
 */
object MyPropsUtils {
  private val bundle: ResourceBundle = ResourceBundle.getBundle("config")
  def apply(propsKey:String):String={
    bundle.getString(propsKey)
  }

}
/*-----------------------------------------------------------------------------------------------------------------*/

import redis.clients.jedis.{Jedis, JedisPool, JedisPoolConfig}

/**
 * Redis工具类，用于获取jedis连接，
 */
object MyRedisUtils {
  var jedisPool: JedisPool = null

  def getJedisFromPool(): Jedis = {
    if(jedisPool == null){
      //创建连接池对象
      //连接池对象
      val jedisPoolConfig = new JedisPoolConfig()
      jedisPoolConfig.setMaxTotal(100) //最大连接数
      jedisPoolConfig.setMaxIdle(20) //最大空闲
      jedisPoolConfig.setMinIdle(20) //最小空闲
      jedisPoolConfig.setBlockWhenExhausted(true) //忙碌时是否等待
      jedisPoolConfig.setMaxWaitMillis(5000) //忙碌时等待时长 毫秒
      jedisPoolConfig.setTestOnBorrow(false) //每次获得连接的进行测试
      val host: String = MyPropsUtils(MyConfig.REDIS_HOST)
      val port: String = MyPropsUtils(MyConfig.REDIS_PORT)
      jedisPool = new JedisPool(jedisPoolConfig,host,port.toInt)
    }
    jedisPool.getResource
  }

}

/*-----------------------------------------------------------------------------------------------------------------*/
case class PageActionLog(
                          mid :String,
                          user_id:String,
                          province_id:String,
                          channel:String,
                          is_new:String,
                          model:String,
                          operate_system:String,
                          version_code:String,
                          brand:String,
                          page_id:String ,
                          last_page_id:String,
                          page_item:String,
                          page_item_type:String,
                          during_time:Long,
                          action_id:String,
                          action_item:String,
                          action_item_type:String,
                          sourceType:String,
                          action_ts:Long,
                          ts:Long
                        ) {
}
/*-----------------------------------------------------------------------------------------------------------------*/
case class PageDisplayLog (
                            mid :String,
                            user_id:String,
                            province_id:String,
                            channel:String,
                            is_new:String,
                            model:String,
                            operate_system:String,
                            version_code:String,
                            brand: String,
                            page_id:String ,
                            last_page_id:String,
                            page_item:String,
                            page_item_type:String,
                            during_time:Long,
                            sourceType:String,
                            display_type:String,
                            display_item: String,
                            display_item_type:String,
                            display_order:String ,
                            display_pos_id:String,
                            ts:Long
                          )
/*-----------------------------------------------------------------------------------------------------------------*/
case class PageLog(
                    mid: String,
                    user_id: String,
                    province_id: String,
                    channel: String,
                    is_new: String,
                    model: String,
                    operate_system: String,
                    version_code: String,
                    brand: String,
                    page_id: String,
                    last_page_id: String,
                    page_item: String,
                    page_item_type: String,
                    during_time: Long,
                    source_time: String,
                    ts: Long
                  ) {}
/*-----------------------------------------------------------------------------------------------------------------*/
case class StartLog(
                     mid :String,
                     user_id:String,
                     province_id:String,
                     channel:String,
                     is_new:String,
                     model:String,
                     operate_system:String,
                     version_code:String,
                     brand:String,
                     entry:String,
                     open_ad_id:String,
                     loading_time_ms:Long,
                     open_ad_ms:Long,
                     open_ad_skip_ms:Long,
                     ts:Long) {
}
/*-----------------------------------------------------------------------------------------------------------------*/
/*
#config.properties 配置文件
kafka.bootstrap-servers=node1:9092,node2:9092,node3:9092
redis.host=node1 
redis.port=6379*/

~~~

