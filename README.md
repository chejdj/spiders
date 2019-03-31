## Spiders  
这个只是为了学习爬虫，自己联系的几个爬虫项目
运行环境: 
**Scrapy 1.6.0**  
**Python 2.7.15**
**BeautifulSoup(HTML解析库)**  
**Request(网络连接库)**  
**Mongo(数据库)**  
**AdminMongo(Mongo可视化界面工具)**  
* 第一步： 安装上面的程序  
* 第二步： 配置并启动数据库  
* 第三步： 启动AdminMongo，看数据库是否连接成功，创建数据库和表格  
* 第四步： `git clone https://github.com/chejdj/spiders.git`  
* 第五步： 修改`settings.py`中的`MONGO_DATABASE`,改为自己数据库的名称，如果自己设置了数据库的url需要修改`MONGO_URI`
* 第五步： 进入该目录执行`scarpy crawl dlut_news`  
自己设置的爬取速率比较低，因为设置过快，自己被封过一次IP  
如果还出错，注意修改`settings.py`中的`DEFAULT_REQUEST_HEADERS`改成自己在浏览器中请求的请求头部信息  
成功之后就可以在数据库中看到数据了  
![result](https://raw.githubusercontent.com/chejdj/DlutNewsSpider/master/images/result.png)  
这个项目目前有3个项目(里面的反爬虫方法比较低级，想学习这方面的，不适合)  
### dlut_news  
爬取的是自己学校官网的学生周知信息   
### zhihu_user  
爬取的是**知乎用户账号信息**  
### android_bus  
爬取的是**安卓巴士网站博客信息**  





