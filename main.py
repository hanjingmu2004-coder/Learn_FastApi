from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse,FileResponse
app = FastAPI()#创建实例 终端运行代码uvicorn main:app --reload


@app.get("/")#定义接口 装饰器=Fastapi实例+请求方法+请求路径
async def root():#异步函数
    return {"message": "Hello World666"}

@app.get("/hello")
async def hello():
    return {"message": "你好"}

@app.get("/user/hello")
async def hello_user():
    return {"msg":"我正在学习FastApi"}

@app.get("/book/{id}")#路径参数 Path添加类型注解
async def get_book(id:int=Path(...,gt=0,lt=101,description="书籍id，取值范围1-100")):
    return {"id":id,"title":f"这是第{id}本书"}

@app.get("/id/{id}")
async def get_id(id:str):
    return {"id":id,"登录信息":f"这是{id}登录信息"}

@app.get("/news/news_list")#查询参数 Query添加类型注解
async def get_news_list(
        skip:int=Query(0,description="跳过的记录数",lt=100),
        limit:int=Query(10,description="返回的记录数")
):
    return {"skip":skip,"limit":limit}

@app.get("/books/booksearch")
async def get_book_search(
        viables:str=Query(...,description="图书分类,长度5-255",min_length=5,max_length=255),
        prices:int=Query(...,description="图书价格50-100",gt=50,lt=100),
):
    return {"viables":viables,"prices":prices}

class User(BaseModel):
    username: str=Field(default="张三",min_length=2,max_length=10)
    password: str=Field(min_length=3,max_length=10)

@app.post("register")#请求体参数
async def register(user:User):
    return user

@app.get("/html",response_class=HTMLResponse)#装饰器指定响应类型
async def get_html():
    return "<h1>这是一级标题</h1>"

@app.get("/file")#返回值定义响应类型
async def get_file():
    path="first.txt"
    return FileResponse(path)

@app.get("/new/{id}")#异常处理
async def get_new(id:int):
    id_list=[1,2,3,4,5]
    if id not in id_list:
        raise HTTPException(status_code=404,detail="您查找到新闻不存在")
    return {"id":id}
