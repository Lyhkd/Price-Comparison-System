### 文件结构



### 项目启动

1. 在根目录下（包含`docker-compose.yml`的目录）进行Docker构建 ，在终端输入`docker-compose up --build`进行构建。如果提示加载错误可以提前下好需要的镜像。
2. mysql数据库文件存放在`sql`目录下，在构建mysql容器使会使用里面的内容进行初始化。已经存在的用户是`guest0`,密码是`123456`。
3. cookie获取，使用浏览器的无痕模式打开https://m.jd.com/，登陆后选择任意一个请求复制cookie存入`back-end/data/JDcookie.txt`文件内。打开https://www.amazon.com/，选择好地址（国家），价格单位（RMB）后存储cookie入`back-end/data/Amazoncookie.txt`内。打开https://www.gwdang.com/，登陆后存储cookie入`back-end/data/GWcookie.txt`内。**配置好cookie后，才可以正常使用实时搜索功能**，否则只能从数据库中获取商品信息。如果依然不成功，可以从`crawler`文件夹中使用各个平台单独的爬虫脚本，测试是否正常。
4. 短信发送提醒功能需要在https://www.smsbao.com/网站充值使用，目前免费额度已经测试用完（😢）

### 前端说明

前端使用 vue3 + vite + axios + pinia + nginx

### 后端说明

后端使用 flask + mysql + celery + redis

### docker使用方法

构建镜像：`docker-compose build`
启动容器：`docker-compose up`
后台运行容器：`docker-compose up -d`
停止容器：`docker-compose down`
查看服务状态：`docker-compose ps`

