import databases
import sqlalchemy
from typing import List, Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


DATABASE_URL = "sqlite:///home_work/home_work_6/my_database.db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

# Таблица должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("lastname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128)),
                         sqlalchemy.Column("passwd", sqlalchemy.String(32)),
                         )
# Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
products = sqlalchemy.Table("products", metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("product_name", sqlalchemy.String(32)),
                            sqlalchemy.Column("description", sqlalchemy.String(128)),
                            sqlalchemy.Column("price", sqlalchemy.Float),
                            )
# Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY),
# id товара (FOREIGN KEY), дата заказа и статус заказа.
orders = sqlalchemy.Table("orders", metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("id_user", sqlalchemy.ForeignKey('users.id')),
                          sqlalchemy.Column("id_product", sqlalchemy.ForeignKey('products.id')),
                          sqlalchemy.Column("order_date", sqlalchemy.DateTime),
                          sqlalchemy.Column("status", sqlalchemy.Boolean),
                          )

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="./home_work/home_work_6/templates")


@app.on_event("startup")
async def startup():
    await database.connect()


# два метода,
# для connect и disconnect БД ! (при запуске создается БД без таблиц, если их нет)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    lastname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    passwd: str = Field(max_length=32)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    lastname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    passwd: str = Field(max_length=32)


class ProductIn(BaseModel):
    product_name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float


class Product(BaseModel):
    id: int
    product_name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float


class OrderIn(BaseModel):
    id_user: int
    id_product: int
    order_date: Optional[datetime] = datetime.now()
    status: bool = Field(default=True)
    # по умолчанию сделка состоялась (раз мы ее добавили)


class Order(BaseModel):
    id: int
    id_user: int
    id_product: int
    order_date: Optional[datetime] = datetime.now()
    status: bool


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    """Create/Добавление пользователя"""
    # query = users.insert().values(name=user.name, email=user.email, lastname=user.lastname, passwd=user.passwd)
    query = users.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), 'id': last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    """Read/Чтение всех пользователей"""
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    """Read/Чтение одного пользователя"""
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    """Update/Обновление пользователя"""
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete/Удаление пользователя"""
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'User deleted': f"ID удаленного пользователя = {user_id}"}


@app.post('/products/', response_model=Product)
async def create_product(user: ProductIn):
    """Create/Добавление товара"""
    query = products.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), 'id': last_record_id}


@app.get("/products/", response_model=List[Product])
async def read_products():
    """Read/Чтение всех продуктов"""
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    """Read/Чтение одного продукта"""
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    """Update/Обновление продукта"""
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    """Delete/Удаление продукта"""
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'Product deleted': f"ID удаленного продукта = {product_id}"}


@app.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    """Create/Добавление заказа"""
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), 'id': last_record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    """Read/Чтение всех заказов"""
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    """Read/Чтение одного заказа"""
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    """Update/Обновление заказа"""
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_product(order_id: int):
    """Delete/Удаление заказа"""
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'order deleted': f"ID удаленного заказы = {order_id}"}
