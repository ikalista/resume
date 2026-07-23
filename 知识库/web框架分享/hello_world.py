# FastAPI 框架
from fastapi import FastAPI
# Pydantic 用于数据校验和序列化
from pydantic import BaseModel, Field

# 创建 FastAPI 应用实例
app = FastAPI()

# ========== 定义请求体模型 ==========
# 继承 BaseModel，字段类型会被自动校验
class Request(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="商品名称") # 必填字段，类型为字符串
    price: float = Field(..., gt=0, description="价格必须大于0") # 必填字段，类型为浮点数
    count: int = Field(default=1, ge=1, le=999, description="数量1-999") # 可选字段，默认值为1


    # Pydantic v2 配置：添加请求示例，会显示在 Swagger 文档中
    model_config = {
        "json_schema_extra": {
            "examples": [{"name": "苹果", "price": 5.5, "count": 10}]
        }
    }

# ========== 定义响应体模型 ==========
class Response(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    price: float = Field(..., gt=0, description="价格必须大于0")
    count: int = Field(default=1, ge=1, le=999, description="数量1-999")
    total: float = Field(..., description="计算后的总价")

    model_config = {
        "json_schema_extra": {
            "examples": [{"name": "苹果", "price": 5.5, "count": 10, "total": 55.0}]
        }
    }

# ========== 定义路由 ==========
# @app.get("/") 是装饰器，表示这是一个 GET 请求，路径为 "/"
@app.get("/")
def hello():
    """这是一个hello接口"""
    # 返回字典，FastAPI 会自动转换为 JSON
    return {"message": "Hello World"}
    

# @app.post("/calculate_total_price") 表示这是一个 POST 请求，路径为 "/calculate_total_price"
# response_model=Response 指定返回值类型，用于生成文档和校验响应
@app.post("/calculate_total_price", response_model=Response)
def calculate_total_price(request: Request):
    """
    计算商品总价
    """
    # 计算总价
    total = request.price * request.count
    # 返回响应模型实例
    return Response(name=request.name, price=request.price, count=request.count, total=total)

# ========== 启动服务 ==========
# 当直接运行此文件时（python hello_world.py），启动服务
# 如果是被其他文件 import，则不会执行
if __name__ == "__main__":
    import uvicorn
    # host="0.0.0.0" 表示监听所有网卡，允许外部访问
    # port=8080 指定端口号
    # 启动后访问 http://127.0.0.1:8080/docs 查看自动生成的 API 文档
    uvicorn.run(app, host="0.0.0.0", port=8080)
