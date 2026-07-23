from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    name: str
    price: float = 5.5
    count: int = 1

class Response(BaseModel):
    name: str
    price: float
    count: int = 1
    total: float

@app.get("/")
def hello():
    return 5

def 模型(price: float, count: int) -> float:
    return price * count

@app.post("/calculate_total_price", response_model=Response)
def calculate_total_price(request: Request):
    
    return Response(name=request.name, price=request.price, count=request.count, total=模型(request.price, request.count))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
