~~~Scala
package bigdata.spark.StreamingHwma

import java.sql.{Connection, DriverManager, PreparedStatement, ResultSet}

/**
 * 使用jdbc访问sparksql的thriftserever
 *
 */
object Demo_ThriftServer {
  def main(args: Array[String]): Unit = {
    //0.加载驱动
    Class.forName("org.apache.hive.jdbc.HiveDriver")
    //1.获取连接
    //访问的是spark的
    val conn: Connection = DriverManager.getConnection("jdbc:hive2://node1:10001/bigdata1", "root", "123456")
    //2.编写SQL
    val sql = """select * from city_info"""
    //3.获取预编译语句对象
    val ps: PreparedStatement = conn.prepareStatement(sql)
    //4.执行SQL
    val rs: ResultSet = ps.executeQuery()
    //5.获取结果
    while (rs.next()) {
      val id: Long = rs.getLong("city_id")
      val name: String = rs.getString("city_name")
      val area: String = rs.getString("area")
      println(s"id:${id},name:${name},area:${area}")
    }
    //6.关闭连接
    if (rs != null) rs.close()
    if (ps != null) ps.close()
    if (conn != null) conn.close()


  }
}

~~~

