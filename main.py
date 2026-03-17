import datetime
from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse,FileResponse
from fastapi import Depends
from sqlalchemy import DateTime, func, String, Float
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
app = FastAPI()#创建实例 终端运行代码uvicorn main:app --reload

#创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:root@localhost:3306/fastapi_first?charset=utf8"
async_engine=create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,#输出日志
    pool_size=10,#允许的连接池最大数量
    max_overflow=20#允许的额外连接数
)
#定义模型类
class Base(DeclarativeBase):#基类：创建时间，更新时间，书籍表：id,书名,作者,价格,出版社
    craete_time:Mapped[datetime]=mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")
    update_time:Mapped[datetime]=mapped_column(DateTime,insert_default=func.now(),default=func.now,onupdate=func.now(),comment="更新时间")


class Book(Base):
    __tablename__ = "book"
    id:Mapped[int]=mapped_column(primary_key=True,comment="书籍id")
    bookname:Mapped[str]=mapped_column(String(255),comment="书名")
    author:Mapped[str]=mapped_column(String(255),comment="作者")
    price:Mapped[float]=mapped_column(Float,comment="价格")
    publisher:Mapped[str]=mapped_column(String(255),comment="出版社")

#建表
async def create_tables():
    #获取异步引擎
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)#Base模型类的元数据创建

@app.on_event("startup")
async def startup():
    await create_tables()

@app.middleware("http")#中间件自底向上响应
async def middleware1(request,call_next):
    print("中间件1 start")
    response=await call_next(request)
    print("中间件1 end")
    return response

@app.middleware("http")
async def middleware1(request,call_next):
    print("中间件2 start")
    response=await call_next(request)
    print("中间件2 end")
    return response

async def common(#依赖项
        skip:int=Query(default=0,ge=0),
        limit:int=Query(default=1,le=60)
):
    return {"skip":skip,"limit":limit}

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
        commons=Depends(common)
):
    return commons

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

#install sqlalchemy[asyncio] aiomysql 创建ORM工具
#建库建表

