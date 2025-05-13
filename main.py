from fastapi import FastAPI, Depends
from typing import Union, Annotated
from sqlmodel import SQLModel, Field, create_engine, Session, select

class Orders(SQLModel, table=True):
    id: int| None = Field(default=None, primary_key=True)
    product_id: str = Field(index=True)
    quantity: int = Field(default=1)


DATABASE_URL = "postgresql://postgres:postgres@db/order_db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
sessionDep = Annotated[Session, Depends(get_session)]
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
    results = session.exec(statement)
    order = results.first()
    if order:
        return order
    else:
        return {"message": "Order not found"}        

@app.get('/orders')
async def get_orders(session: sessionDep):
    statement = select(Orders)
    results = session.exec(statement)
    orders = results.all()
    if orders:
        return orders
    else:
        return{"message": "Orders not found"}
