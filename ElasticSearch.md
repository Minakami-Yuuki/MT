## 						服务器中配置ElasticSearch

#### 1. 创建目录存放es：

```
	cd /usr/local
	mkdir elasticsearch
```

#### 2. 下载es压缩包：

```
	wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.15.1-linux-x86_64.tar.gz
```

#### 3.解压并移动至新建目录

```
	tar -zxvf elasticsearch-7.15.1-linux-x86_64.tar.gz
	mv elasticsearch-7.15.1 /usr/local/elasticsearch
	(默认：创建两个文件夹)
	mkdir /usr/local/elasticsearch/data #数据目录
	mkdir /usr/local/elasticsearch/logs #日志目录
```

#### 4. 创建集群 (es默认不允许root用户使用)

```
	groupadd es
	useradd es
	passwd es
	(psw: elasticsearch)
```

#### 5. 修改配置文件.yml	(: 后需要加空格)

```
	cluster.name: my-es
	#节点名称
	node.name: node-1
	#设置索引数据的存储路径
	path.data: /usr/local/elasticsearch/data
	#设置日志的存储路径
	path.logs: /usr/local/elasticsearch/logs
	#设置当前的ip地址,通过指定相同网段的其他节点会加入该集群中
	network.host: 0.0.0.0
	#设置对外服务的http端口
	http.port: 9200

	#设置master节点列表 用逗号分隔
	cluster.initial_master_nodes: ["node-1", "node-2"]
```

#### 6. 重新分配权限	(将elasticsearch文件从root移交至es)

```
	chown -Rf es:es elasticsearch
	chown 777 -R elasticsearch
	(chmod 777 -R data)
```

#### 7. 修改系统文件

```
	vim /etc/security/limits.conf
	# 增加操作空间
	# End of file
	root soft nofile 65535
	root hard nofile 65535
	* soft nofile 65536
	* hard nofile 65536
	es soft nofile 65536
	es hard nofile 65536
	es soft nproc 4096
	es hard nproc 4096
```

```
	vim /etc/sysctl.conf
	# 文件中写入如下内容 增加最大运行内存
	vm.max_map_count=65536 (或262144)
	# 刷新内存
	sysctl -p
```

#### 8. 启动和关闭es

```
启动：
	#切换用户
	su es
	cd /usr/local/elasticsearch/elasticsearch-7.15.1/bin
	./elasticsearch -d
```

```
若启动成功：
	采用curl命令显示：
	curl 'http://localhost:9200'
	或输入 “180.76.156.218:9200”
即可显示：
	{
  "name" : "node-1",
  "cluster_name" : "my-es",
  "cluster_uuid" : "_na_",
  "version" : {
    "number" : "7.15.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "83c34f456ae29d60e94d886e455e6a3409bba9ed",
    "build_date" : "2021-10-07T21:56:19.031608185Z",
    "build_snapshot" : false,
    "lucene_version" : "8.9.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

```
关闭es：
	ps -ef | grep elasticsearch #查找es进程
	kill -9 PID	#杀死对应进程即可关闭
```

