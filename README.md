# vruc_scrapy
从微人大(中国人民大学教务网站)上抓取个人成绩，并保存在items.json文件中。
## 需要安装下列软件
- Python 2.7
- Scrapy 1.0.5

## 运行
在项目根路径下,输入一下命令：
> scrapy crawl vruc

然后在运行过程中输入微人大用户名和密码，成绩会以json的格式保存在根目录下的items.json中

## 注意
没错，需要联网
