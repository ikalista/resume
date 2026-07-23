## 1. CPU密集型 vs IO密集型

+ **CPU密集型**: 模型推理，图像处理，CPU需要大量运转。
+ **IO密集型**：访问他人接口，访问数据库，读写文件，别人的CPU需要大量运转，我们的CPU在等待。

## 2. 什么是同步, 什么是异步, 什么是线程, 什么是协程

同步就是运行到那会阻塞的代码, 大多数代码都是同步的, 例如

```python
df = pd.read_csv("lol.csv")
```

异步就是需要借助asyncio库支持, 涉及原生关键词async, await的代码，异步代码需要放入一个事件循环执行：

```python
async def insert_get_score_log(get_score_call: ScoreCall, response, reRankedProductList):
	connection = await asyncpg.connect(**pg_config)
    data = ...
    insert_query = f'''INSERT INTO get_score_log ({columns_str}) VALUES ({占位符_str})'''
    await connection.execute(insert_query, *data.values())
    await connection.close()
asyncio.run(insert_get_score_log(score_call, response, reRankedProductList)) # 使用默认的事件循环
```

同步和异步在并发时候有所不同：

+ 同步代码使用多线程进行多并发时，起线程会调用系统接口，分配系统资源给线程，调度也是交给系统来做的。
+ 异步代码使用协程进行多并发，基于事件循环，起协程都是在程序内的，是用户态的，系统无感知。

为什么说协程就是单线程，因为事件循环就是一个线程

## 3. WSGI & ASGI

+ **WSGI** 服务器网关接口(Web Server Gateway Interface，WSGI)：单调用、同步接口，即输入一个请求，返回一个响应，代表：uWSGI，gunicorn，Werkzeug(Flask自带的那位)
+ **ASGI** 异步服务器网关接口(Asynchronous Server Gateway Interface)：长连接、异步接口，支持websocket等新兴协议，代表：uvicorn

ASGI是WSGI的继任者。在 Web 2.0时代，WSGI完美地承载了我们的业务，随着移动网络的发展，Web技术也在升级，比如WebSocket、HTTP/2，HTTP/3

+ WSGI应用框架: Django, Flask
+ ASGI应用框架: Fastapi, Sanic

### 3.1 最简单的WSGI应用

```python
def application(environ, start_response):
    # do something on the request context variable: environ
    return start_response("200 OK")
```

### 3.2 最简单的ASGI应用

```python
async def application(scope, receive, send):
    event = await receive()
    ...
    await send({"type": "websocket.send", ...})
```

只要按照以上协议编写的代码都可以作为这两种不同的web应用

## 4. Web框架：如何和Socket交互

+ socket -> wsgi -> wsgiApp： wsgi首先会启动一个socket服务器监听你设定的端口，然后每个请求分配一个线程去执行响应。
+ socket -> asgi -> asgiApp： asgi首先会启动一个socket服务器监听端口，然后启动事件循环，每个请求到来分配一个协程去执行响应。

### 4.1 WSGI服务持久化

以flask为例 werkzeug会启动一个ThreadedWSGIServer，ThreadedWSGIServe继承ThreadingMixIn, BaseWSGIServer赋予该类与socket交互的能力，继承自socketserver库 ThreadingMixIn赋予该类多线程执行的能力：

```python
werkzeug.serving.run_simple(host, port, app, **options)
```

```python
ThreadingMixIn.process_request():
t = threading.Thread(target = self.process_request_thread, args = (request, client_address))
```

### 4.2 WSGI处理请求

werkzeug在处理完socket的请求后，按照wsgi协议：application(environ, start_response) 调用 flask的app

![](https://cdn.nlark.com/yuque/0/2024/png/40755316/1706095155805-d02eb188-3eae-4038-83e1-fd5a536cc117.png)

app根据environ对象，根据用户声明好的路由/endpoint/，转发到用户定义的方法

![](https://cdn.nlark.com/yuque/0/2024/png/40755316/1706095167011-9e5d88e9-d52a-4642-bd44-ef8f0d646466.png)

在用户返回后，调用start_response为用户的返回进行包装, 一个完整的请求就完成了

### 4.3 ASGI服务持久化

```python
uvicorn.run()
def run(self, sockets=None):
    self.config.setup_event_loop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(self.serve(sockets=sockets))
```

uvicorn会启动一个事件循环, 持续的监听端口:

![](https://cdn.nlark.com/yuque/0/2024/png/40755316/1706095179812-785f7dbf-5060-4133-92e0-95860795b341.png)

### 4.4 ASGI处理请求

uvicorn包装好请求到scope, receive, send后，用类似于wsgi的方法调用fastapi的用户定义的app对象，接着转发到用户注册的路由方法，就是我们经常看到的注解

![](https://cdn.nlark.com/yuque/0/2024/png/40755316/1706095436640-05eb175a-9122-4fb8-a721-7727aec1a6d1.png)

fastapi会根据scope, send的内容来处理请求，并调用send进行响应，一个完整的请求就完成了 从逻辑上唯一和flask不同的地方在于，异步会将自己的控制权交出，所以需要有持续的receive和send方法来作为通道传输，而wsgi的environ完成了asgi scope+receive的功能

## 5. 性能测试

我对三个框架进行了相同的两个测试，并发都是10 cpu密集型是对一个1000*1000的矩阵进行了相乘 io密集型是对一个固定响应1s时间的接口进行了访问 可以看到在cpu密集型，flask的响应时间最快，fastapi和sanic略微逊色。

![](https://cdn.nlark.com/yuque/0/2024/png/40755316/1706095454836-5aea2ddf-ef4c-4031-be26-39fa1ef3e37b.png)

而在io密集型上，fastapi和sanic(平均1004ms)更快，flask(1037ms)稍显逊色

![](https://cdn.nlark.com/yuque/0/2024/png/40755316/1706095469595-5e8d7d41-38f4-438d-8471-da397b701c57.png)

这也符合我们的预期： 异步单线程在执行cpu密集型的时候反而会吃力，wsgi应用>asgi应用 而多线程应用在io密集型的时候开启了过多的协程进行上下文切换，会浪费资源造成响应缓慢, asgi应用>wsgi应用

## 6. 性能之外

+ **FastAPI** 是目前最风靡框架，特点是swagger的自动集成赋予它自动的api文档生成能力，基于pydantic的参数校验能力，以及asgi应用都具有的和websocket等新协议建立长连接的能力，如果你需要和类似的协议做交互，fastapi是不可或缺的。
+ **Sanic** 出生比较早，python3.5，异步生态还没有建好时，就自己完成了很多的异步工作。更原生的代码，再加上没有很多的参数校验以及文档生成的功能，在当时运行效率是fastapi的1.5倍，但不是数量级上的差异。
+ **Flask** 是wsgi下最风靡最轻量的框架, 有很强的扩展能力，集成wsgi以及jinja模板，使得我们可以很快的搭建前后端不分离的简易网页。

## 7. Pydantic与类型校验

### 7.1 什么是Pydantic

Pydantic 是一个基于 Python 类型注解的数据校验库，FastAPI 的参数校验能力完全依赖于它。

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    count: int = 1
```

当请求数据不符合定义时，Pydantic 会自动返回清晰的错误信息，无需手动编写校验逻辑。

### 7.2 强制类型校验的好处

+ **防御性编程**：接口入参在进入业务逻辑前就已经被校验，避免脏数据进入系统
+ **减少样板代码**：不需要写 `if not isinstance(...)` 或 `if xxx is None` 这类校验代码
+ **自动类型转换**：传入 `"123"` 会自动转成 `123`（int类型），传入 `"abc"` 则报错
+ **IDE友好**：类型注解让 IDE 可以提供自动补全和错误提示
+ **文档自动生成**：类型信息会被 FastAPI 提取，自动生成 API 文档的 Schema

### 7.3 常用校验能力

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    price: float = Field(..., gt=0, description="价格必须大于0")
    count: int = Field(default=1, ge=1, le=999, description="数量1-999")
```

+ `...` 表示必填
+ `gt/ge/lt/le` 数值范围校验
+ `min_length/max_length` 字符串长度校验
+ `description` 会显示在自动生成的文档中

## 8. 上下游联调

在微服务架构下，服务之间的接口对接是一个常见痛点：

+ 接口文档和代码不同步，文档写了但代码改了没更新
+ 上下游对接需要反复沟通确认参数格式
+ 接口变更后，调用方不知道该怎么改

FastAPI 通过 **代码即文档** 的方式解决了这个问题：

### 8.1 自动生成交互式文档

FastAPI 内置了两种自动文档：

+ **Swagger UI**：访问 `/docs`，可以直接在页面上测试接口
+ **ReDoc**：访问 `/redoc`，更适合阅读的文档格式

### 8.2 代码即文档

FastAPI 基于 Python 类型注解和 Pydantic 模型，自动提取以下信息生成文档：

+ 请求参数类型、是否必填、默认值
+ 请求体的 JSON Schema
+ 响应体的结构和示例
+ 接口描述（从 docstring 提取）

这意味着：**只要代码写对了，文档就是对的**，不存在文档和代码不同步的问题。

### 8.3 联调流程

1. 后端开发完接口，直接把 `/docs` 地址发给前端或上游服务
2. 对方在 Swagger UI 上直接试用接口，了解参数格式
3. 接口变更时，文档自动更新，对方刷新页面即可看到最新定义

启动后访问 `http://127.0.0.1:8000/docs` 即可看到自动生成的接口文档

## 9. 总结

1. 使用fastapi作为唯一的web框架选择，因为它在实用性，上下游联调，及性能上权衡下来是最优的
2. 禁止使用async关键词（性能确实高，但是如果用法不对会导致整个服务锁死）
3. 使用pydantic模型进行链路串联及多人协作
4. Web框架请求全流程：
   ```
   Socket while True 监听端口
           ↓
   WSGI/ASGI 捕获请求，封装上下文（environ / scope+receive）
           ↓
   路由分发，执行用户代码，拿到结果
           ↓
   调用响应方法（start_response / send）返回数据
           ↓
   上游拿到结果
   ```
