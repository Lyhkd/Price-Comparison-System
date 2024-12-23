## 后端说明

### 后端概述

后端使用了Flask框架，Mysql作为数据库，并集成了Celery用于异步任务处理。

### 结构说明

```python
back-end
├─ Dockerfile
├─ README.md
├─ app
│  ├─ __init__.py
│  ├─ celeryconfig.py
│  └─ config.py
├─ celery_route
│  ├─ __init__.py
│  └─ test.py
├─ celerybeat-schedule.db
├─ controllers
│  ├─ __init__.py
│  ├─ alert_controller.py
│  ├─ item_controller.py
│  ├─ platform_controller.py
│  ├─ price_controller.py
│  └─ user_controller.py
├─ data
│  ├─ Amazoncookie.txt
│  ├─ GWcookie.txt
│  └─ JDcookie.txt
├─ models
│  ├─ __init__.py
│  ├─ item.py
│  ├─ platform.py
│  ├─ price_alert.py
│  ├─ price_history.py
│  ├─ search_history.py
│  └─ user.py
├─ requirements.txt
├─ routes
│  ├─ __init__.py
│  ├─ alert.py
│  ├─ search.py
│  └─ user.py
├─ run.py
└─ utils
   ├─ __init__.py
   ├─ auth.py
   ├─ crawler.py
   └─ tasks.py
```

1. app内存放了初始化flask、celery、mysql等功能的代码，config文件配置了网络参数
2. data内存放了各个电商网站的cookie
3. controllers主要负责实现和各个数据库model的交互
4. models内定义了各个table的数据
5. routes内定义了后端如何接收前端的请求以及各个api的情况
6. utils中实现了爬虫功能、celery的异步检查价格功能和发送短信邮件功能

### 主要功能

#### 用户管理

用户可以注册、登录和更新个人信息。用户信息包括用户名、密码、邮箱和手机号码。

**实现方法：**

- 用户注册：`/user/signup` 路由处理用户注册请求，检查用户名、密码和邮箱是否存在，并将用户信息存储在数据库中。
- 用户登录：`/user/login` 路由处理用户登录请求，验证用户名和密码，并生成JWT令牌。
- 更新用户信息：`/user/auth/loginInfo` 路由处理用户信息更新请求，使用JWT令牌验证用户身份，并更新用户信息。

#### 商品管理

平台支持从多个电商平台（如京东、亚马逊）抓取商品信息，并存储在数据库中。用户可以搜索商品，查看商品详情和价格历史。

**实现方法：**

- 搜索商品：`/search` 路由处理商品搜索请求，支持分页和排序，并异步抓取更多数据。
- 获取商品详情：`/item/<id>` 路由处理商品详情请求，返回商品的详细信息，同时使用celery异步更新商品的价格信息。
- 获取商品价格历史：`/item/price/<id>` 路由处理商品价格历史请求，返回商品的价格变化记录。

#### 价格提醒

用户可以为商品设置价格提醒，当商品价格达到目标价格时，系统会通过邮件或短信通知用户。

**实现方法：**

- 添加价格提醒：`/alert` 路由处理添加价格提醒请求，检查是否已存在相同的提醒，并将提醒信息存储在数据库中。
- 查询用户提醒：`/alert/<uid>` 路由处理查询用户提醒请求，返回用户的所有价格提醒。
- 更新价格提醒：`/alert/<alertid>` 路由处理更新价格提醒请求，修改提醒的目标价格和通知方式。
- 删除价格提醒：`/alert/<alert_id>` 路由处理删除价格提醒请求，删除指定的价格提醒。
- 发送通知：`/alert/sendemail` 和 `/alert/sendsms` 路由处理发送邮件和短信通知请求。

#### 平台管理

管理支持的电商平台信息，包括平台名称和Logo URL。

**实现方法：**

- 获取平台名称：`get_platform_name` 函数根据平台ID返回平台名称。
- 获取平台ID：`get_platform_id` 函数根据平台名称返回平台ID，如果平台不存在则创建新平台。
- 获取平台Logo URL：`get_platform_url` 函数根据平台ID返回平台的Logo URL。

#### 异步任务

使用Celery处理异步任务，如定时检查商品价格。

**实现方法：**

- 定时任务：配置`celery_beat`，执行`check_price` 函数定时检查商品价格，并触发价格提醒。

### 数据库范式

| 表名  | 字段        | 数据类型     | 约束                                                         | 解释                                   |
| ----- | ----------- | ------------ | ------------------------------------------------------------ | -------------------------------------- |
| users | id          | Integer      | primary_key=True, autoincrement=True                         | 用户ID，主键，自增                     |
|       | uid         | String(8)    | unique=True, nullable=False, index=True                      | 用户唯一标识，唯一，非空，索引         |
|       | username    | String(64)   | unique=True, nullable=False, index=True                      | 用户名，唯一，非空，索引               |
|       | password    | String(256)  | nullable=False                                               | 用户密码，非空                         |
|       | email       | String(120)  | unique=True, nullable=False, index=True                      | 用户邮箱，唯一，非空，索引             |
|       | created_at  | DateTime     | default=datetime.utcnow                                      | 创建时间，默认当前时间                 |
|       | updated_at  | DateTime     | default=datetime.utcnow, onupdate=datetime.utcnow            | 更新时间，默认当前时间，更新时自动更新 |
|       | avatar      | String(128)  | nullable=False, default='[https://cdn.pixabay.com/photo/2018/11/13/22/01/avatar-3814081_1280.png](vscode-file://vscode-app/Applications/Visual Studio Code.app/Contents/Resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)' | 用户头像，非空，默认值                 |
|       | phone       | String(20)   | unique=True, nullable=True                                   | 用户手机号码，唯一，可空               |
|       | alert_lists | Relationship | -                                                            | 用户的价格提醒列表                     |

| 表名          | 字段        | 数据类型       | 约束                                                 | 解释                   |
| ------------- | ----------- | -------------- | ---------------------------------------------------- | ---------------------- |
| price_history | id          | Integer        | primary_key=True, autoincrement=True                 | 价格历史ID，主键，自增 |
|               | item_id     | Integer        | ForeignKey('items.id'), nullable=False               | 商品ID，外键，非空     |
|               | platform_id | Integer        | ForeignKey('platforms.id'), nullable=False           | 平台ID，外键，非空     |
|               | price       | Numeric(10, 2) | nullable=False                                       | 价格，非空             |
|               | date        | TIMESTAMP      | default=datetime.utcnow                              | 日期，默认当前时间     |
|               | -           | -              | Index('idx_item_platform', 'item_id', 'platform_id') | 索引，组合索引         |
|               | -           | -              | Index('idx_created_at', 'date')                      | 索引，日期索引         |

| 表名         | 字段                | 数据类型   | 约束                                                         | 解释                                             |
| ------------ | ------------------- | ---------- | ------------------------------------------------------------ | ------------------------------------------------ |
| price_alerts | id                  | Integer    | primary_key=True                                             | 价格提醒ID，主键                                 |
|              | user_id             | Integer    | ForeignKey('users.id'), nullable=False                       | 用户ID，外键，非空                               |
|              | item_id             | Integer    | ForeignKey('items.id'), nullable=False                       | 商品ID，外键，非空                               |
|              | target_price        | Float      | nullable=False                                               | 目标价格，非空                                   |
|              | created_at          | DateTime   | default=datetime.utcnow                                      | 创建时间，默认当前时间                           |
|              | updated_at          | DateTime   | default=datetime.utcnow                                      | 更新时间，默认当前时间                           |
|              | enable              | Boolean    | default=True                                                 | 启用状态，默认启用                               |
|              | check_interval      | Integer    | default=15                                                   | 检查间隔，单位：分钟，默认15分钟                 |
|              | notification_method | String(50) | nullable=False                                               | 通知方式，非空                                   |
|              | -                   | -          | UniqueConstraint('user_id', 'item_id', name='uix_user_item') | 唯一约束，确保同一用户对同一商品只能设置一个提醒 |

| 表名          | 字段        | 数据类型       | 约束                                                         | 解释                             |
| ------------- | ----------- | -------------- | ------------------------------------------------------------ | -------------------------------- |
| alert_history | id          | Integer        | primary_key=True, autoincrement=True                         | 提醒历史ID，主键，自增           |
|               | alert_id    | Integer        | ForeignKey("price_alerts.id", ondelete='CASCADE'), nullable=False | 价格提醒ID，外键，非空，级联删除 |
|               | price_after | Numeric(10, 2) | nullable=False                                               | 价格变化后，非空                 |
|               | created_at  | DateTime       | default=datetime.utcnow                                      | 创建时间，默认当前时间           |
|               | -           | -              | Index('idx_alert', 'alert_id')                               | 索引，提醒ID索引                 |
|               | -           | -              | Index('idx_created_at', 'created_at')                        | 索引，创建时间索引               |

| 表名      | 字段     | 数据类型    | 约束                                    | 解释                       |
| --------- | -------- | ----------- | --------------------------------------- | -------------------------- |
| platforms | id       | Integer     | primary_key=True, autoincrement=True    | 平台ID，主键，自增         |
|           | name     | String(50)  | unique=True, nullable=False, index=True | 平台名称，唯一，非空，索引 |
|           | logo_url | String(255) | -                                       | 平台Logo URL               |

| 表名  | 字段          | 数据类型     | 约束                                      | 解释                   |
| ----- | ------------- | ------------ | ----------------------------------------- | ---------------------- |
| items | id            | Integer      | primary_key=True                          | 商品ID，主键           |
|       | title         | String(200)  | nullable=False                            | 商品标题，非空         |
|       | search_title  | String(255)  | nullable=False                            | 搜索标题，非空         |
|       | link          | String(255)  | nullable=False                            | 商品链接，非空         |
|       | image_url     | String(255)  | nullable=True                             | 商品图片URL，可空      |
|       | create_time   | DateTime     | default=datetime.utcnow                   | 创建时间，默认当前时间 |
|       | update_time   | DateTime     | default=datetime.utcnow                   | 更新时间，默认当前时间 |
|       | current_price | Float        | nullable=False                            | 当前价格，非空         |
|       | platform_id   | Integer      | ForeignKey('platforms.id'), nullable=True | 平台ID，外键，可空     |
|       | shop          | String(255)  | nullable=True                             | 店铺信息，可空         |
|       | shop_link     | String(255)  | nullable=True                             | 店铺链接，可空         |
|       | sku           | String(255)  | nullable=False, unique=True               | SKU，唯一，非空        |
|       | description   | String(2048) | nullable=True                             | 商品描述，可空         |

## 前端说明

### 结构说明

```text
front-end
├─ Dockerfile
├─ README.md
├─ auto-imports.d.ts
├─ components.d.ts
├─ default.conf
├─ index.html
├─ package.json
├─ public
│  └─ favicon.ico
├─ src
│  ├─ App.vue
│  ├─ api
│  │  ├─ index.ts
│  │  └─ request.ts
│  ├─ assets
│  │  └─ images
│  ├─ components
│  │  ├─ PriceChart
│  │  │  └─ index.vue
│  │  ├─ footer
│  │  │  └─ Footer.vue
│  │  ├─ header
│  │  │  └─ index.vue
│  │  └─ message
│  │     └─ index.vue
│  ├─ config
│  ├─ env.d.ts
│  ├─ libs
│  │  ├─ token.ts
│  │  └─ utils.ts
│  ├─ main.ts
│  ├─ mock
│  │  ├─ home
│  │  │  ├─ banner.json
│  │  │  └─ floor.json
│  │  ├─ home.ts
│  │  └─ user.ts
│  ├─ router
│  │  └─ index.ts
│  ├─ store
│  │  ├─ alerts.ts
│  │  ├─ item.ts
│  │  ├─ login.ts
│  │  ├─ search.ts
│  │  └─ user.ts
│  ├─ styles
│  ├─ types
│  │  ├─ index.ts
│  │  ├─ login
│  │  │  └─ index.ts
│  │  ├─ search
│  │  │  └─ index.ts
│  │  └─ user
│  │     └─ index.ts
│  └─ views
│     ├─ home
│     │  ├─ index.vue
│     │  ├─ product-card
│     │  │  └─ index.vue
│     │  └─ search-bar
│     │     └─ index.vue
│     ├─ item
│     │  ├─ PriceChart
│     │  │  └─ index.vue
│     │  └─ index.vue
│     ├─ price-alert
│     │  ├─ PriceChart
│     │  │  └─ index.vue
│     │  ├─ UserPanel
│     │  │  └─ index.vue
│     │  └─ index.vue
│     ├─ register
│     │  └─ index.vue
│     └─ search
│        └─ index.vue
├─ tsconfig.json
└─ vite.config.ts

```

1. Components：采用组件化设计，将页面拆分为多个独立的组件，便于维护和复用。`Header、Footer、PriceChart`等组件分别实现各自的功能。

2. Store：使用 Pinia 进行状态管理，将全局状态存储在 `store` 目录下的各个模块中。例如，`login.ts` 管理登录状态，`search.ts` 管理搜索状态，`alerts.ts` 管理价格提醒状态。
3. Router：用 Vue Router 进行路由管理，将不同的页面和组件通过路由进行连接。路由配置文件位于 [index.ts](vscode-file://vscode-app/Applications/Visual Studio Code.app/Contents/Resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)，定义了各个页面的路由规则。

4. api：将所有的 API 请求封装在`api`目录下，通过`request.ts`进行统一管理。使用 Axios 进行 HTTP 请求，并在请求和响应拦截器中处理通用逻辑。
5. View：借助vue框架实现了各个页面的内容以及函数逻辑

