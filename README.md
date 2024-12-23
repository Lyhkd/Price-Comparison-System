### 项目启动

1. 在根目录下（包含`docker-compose.yml`的目录）进行Docker构建 ，在终端输入`docker-compose up --build`进行构建。如果提示加载错误可以提前下好需要的镜像。
2. mysql数据库文件存放在`sql`目录下，在构建mysql容器使会使用里面的内容进行初始化。已经存在的测试用户是`lyhkd0`,密码是`123456`。
3. cookie获取，使用浏览器的无痕模式打开https://m.jd.com/，登陆后选择任意一个请求复制cookie存入`back-end/data/JDcookie.txt`文件内。打开https://www.amazon.com/，选择好地址（国家），价格单位（RMB）后存储cookie入`back-end/data/Amazoncookie.txt`内。打开https://www.gwdang.com/，登陆后存储cookie入`back-end/data/GWcookie.txt`内。**配置好cookie后，才可以正常使用实时搜索功能**，否则只能从数据库中获取商品信息。如果依然不成功，可以从`crawler`文件夹中使用各个平台单独的爬虫脚本，测试是否正常。
4. 短信发送提醒功能需要在https://www.smsbao.com/网站充值使用，目前免费额度已经测试用完（😢）

### 使用说明

在网站的home页可以直接进行商品搜索

![image-20241222164841699](assets/image-20241222164841699.png)

在注册页输入合法的用户名、邮箱、密码可以实现注册

![image-20241222165144954](assets/image-20241222165144954.png)

在用户登录页面输入账户信息即可登录

![image-20241222165014412](assets/image-20241222165014412.png)

登录后个人信息会显示在右上角，并且可以收藏商品。可以通过个人设置修改账户内容。

![image-20241222165238501](assets/image-20241222165238501.png)

<img src="assets/image-20241222165300229.png" alt="image-20241222165300229" style="zoom:50%;" />

<img src="assets/image-20241222165343886.png" alt="image-20241222165343886" style="zoom:50%;" />

商品页面会如果没有进行搜索会随机展示一些商品，可以选择平台、价格进行筛选排序

![image-20241222165515949](assets/image-20241222165515949.png)

在商品展示页会显示商品的详情、价格趋势图等。（第一次加载商品时如果详情为空，**可以等待一段时间后刷新**。查看从网站爬取的价格和商品详情）。在每次搜索/展示商品时都会更新历史价格数据。

![image-20241222165637872](assets/image-20241222165637872.png)

点击添加价格提醒即可加入收藏夹（如果未登录会跳转到登陆界面）

![image-20241222165756615](assets/image-20241222165756615.png)

在设置价格提醒中可以选择价格的具体提醒点以及提醒方式。

![image-20241222165928703](assets/image-20241222165928703.png)

添加成功后会在个人页面展示所有添加的商品并且允许修改提醒方式/价格/是否启动提醒等。对于已经提醒过的商品会显示提醒的历史记录。

![image-20241222170150598](assets/image-20241222170150598.png)

![image-20241222170129786](assets/image-20241222170129786.png)

价格波动后会在邮箱或短信收到提醒。

<img src="assets/image-20241222170254232.png" alt="image-20241222170254232" style="zoom:50%;" />

<img src="assets/image-20241222170347022.png" alt="image-20241222170347022" style="zoom:50%;" />

### docker使用方法

构建镜像：`docker-compose build`
启动容器：`docker-compose up`
后台运行容器：`docker-compose up -d`
停止容器：`docker-compose down`
查看服务状态：`docker-compose ps`

