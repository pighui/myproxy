# myproxy
一个免费的IP代理池

预览地址：[点击这里](http://122.112.231.109:8888/ip/random/)  **单机勿压**

如果对您有帮助，希望给个 Star ⭐，谢谢！😁😘🎁🎉

Github 项目地址 ：[pighui](https://github.com/pighui)/[myproxy](<https://github.com/pighui/myproxy>)

# 简介

​	在我们爬取一个网站的时候，频繁的请求容易导致ip被ban，使用ip代理我们的请求可以绕过这种反爬策略。IP代理池则可以满足我们的这种需求。

**PS**：此项目仅供学习使用和参考。

# 项目结构

![](test_imgs/project.png)

# 克隆项目

```bash
git clone git@github.com:pighui/myproxy.git
```

# 项目启动

## 1.安装Python

至少python3.5以上

## 2.安装mysql

至少mysql3.7以上

### 3.修改配置文件

修改项目根目录下的settings.py文件

### 4.安装依赖包

```bash
cd myproxy
pip3 install -r requirements.txt
```

### 5.启动项目

```bash
python3 run.py
```

# 获取代理

## 脚本示例（详见接口说明）

脚本已上传至项目根目录（get_proxy.py）

```python
import requests


def get_proxies(params: dict = {}):
    '''
    :param params: 参数字典 默认为空
    :return: 返回一个包含多条代理信息的列表，列表的每一个元素是一个字典
    '''
    try:
        response = requests.get('http://127.0.0.1:8888/ip/', params=params)
        if response.status_code == 200:
            result = response.json()
            return [{d['protocol']: 'http://' + d['ip'] + ':' + d['port']} for d in result]
    except ConnectionError:
        return None


def random_proxy():
    '''
    :return: 返回一个代理信息字典
    '''
    try:
        response = requests.get('http://127.0.0.1:8888/ip/random/')
        if response.status_code == 200:
            result = response.json()
            return result
    except ConnectionError:
        return None
```

# 接口说明

## 1.获取最快的一个代理

接口：http://127.0.0.1:8888/ip/

请求方式：GET

调用示例：

![](test_imgs/getone.png)

## 2.随机获取一个代理

接口：http://127.0.0.1:8888/ip/random/

请求方式：GET

调用示例：

![](test_imgs/random.png)

## 3.获取指定数量、指定协议、指定匿名度的排名前几的几条代理

接口：http://127.0.0.1:8888/ip/?protocol=&anonymity=&count=

请求方式：GET

路由参数：

- protocol 协议类型，可选http/https，默认值http
- anonymity 匿名度，可选1/0(高匿/透明)，默认值1
- count 数量，即获取代理的条数，默认值1

调用示例：

![](test_imgs/get.png)

## 4.获取数据库中的所有代理

接口：http://127.0.0.1:8888/ip/all/

请求方式：GET

调用示例：

![](test_imgs/getall.png)

## 5.增加一条代理到数据库

接口：http://127.0.0.1:8888/ip/

请求方式：POST

表单参数:ip，port，protocol，anonymity，score

调用示例：

![](test_imgs/post.png)

## 6.更新数据库中的一条代理

接口：http://127.0.0.1:8888/ip/

请求方式：PUT

表单参数：ip，port，protocol，anonymity，score

调用示例：

![](test_imgs/put.png)

## 7.删除数据库中的一条代理

接口：http://127.0.0.1:8888/ip/string:ip/

请求方式：DELETE

路由参数：ip

调用示例：

![](test_imgs/delete.png)

# 写在最后

​	FreeIPWeb.txt使我目前爬取的提供免费IP代理的网站，如果你知道其他还不错的免费代理网站，可以在issues里提交，当然也可以给我发email，我会把它添加到这个项目里。