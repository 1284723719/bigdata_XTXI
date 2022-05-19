# grafana安装

- 下载grafana-7.5.3-1.x86_64.rpm软件

    -  https://dl.grafana.com/oss/release/grafana-7.5.3-1.x86_64.rpm

- 上传rpm包，安装grafana

    ```shell
    rz grafana-7.5.3-1.x86_64.rpm /root
    rpm -ivh grafana-7.5.3-1.x86_64.rpm
    ```

- 启动服务

    ```shell
    # 设置开机自启动
    systemctl enable grafana-server
    # 启动服务
    systemctl start grafana-server
    # 查看服务状态
    systemctl status grafana-server
    ```

- 访问服务页面

    - http://node1:3000/

        ![](https://s2.loli.net/2022/05/19/oeXrRc7yECv5GNT.png)