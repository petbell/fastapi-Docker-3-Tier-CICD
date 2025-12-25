from fastapi import FastAPI, Depends
from typing import Union, Annotated
from sqlmodel import SQLModel, Field, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

class Orders(SQLModel, table=True):
    id: int| None = Field(default=None, primary_key=True)
    product_id: str = Field(index=True)
    quantity: int = Field(default=1)


#DATABASE_URL = "postgresql://postgres:postgres@db/order_db"
# for localhost
DATABASE_URL = "postgresql+psycopg://petbell:i12pose@localhost/order_db"
engine = create_async_engine(DATABASE_URL, echo=True, # set to false in production
                             future=True)
# All the jara async session stuff was becuase of async support in sqlmodel
# if not, all you need is to add "+psycopg" to the database url and use normal sessionmaker
AsyncSessionLocal = sessionmaker(bind=engine, 
                            class_=AsyncSession, 
                            expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

sessionDep = Annotated[AsyncSession, Depends(get_session)]
create_db_and_tables()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{itemid}")
def read_items(itemid: int, q: Union [str, None] =  None):
    return {"item_id": itemid, "Q": q }
        
@app.get("/orders/{order_id}")
async def get_an_order(order_id: int, session: sessionDep):
    statement = select(Orders).where(Orders.id == order_id)
    results = await session.exec(statement)
    order = results.first()
    if order:
        return order
    else:
        return {"message": "Order not found"}        

@app.get('/orders')
async def get_orders(session: sessionDep):
    statement = select(Orders)
    print ("about to execute statement")
    results = await session.exec(statement)
    print ("statement executed")
    print (results)
    orders = results.all()
    if orders:
        return orders
    else:
        return{"message": "Orders not found"}

@app.post('/orders')
async def create_order(order: Orders, session: sessionDep):
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return {"message" : order}