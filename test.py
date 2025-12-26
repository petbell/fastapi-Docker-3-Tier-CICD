from fastapi import FastAPI
from models import Product
import asyncio
from time import sleep
app = FastAPI()

products = []

@app.get("/")
async def root():
    return {"message": "Hello Peter"}

# get all products
@app.get("/products")
async def get_all_products():
        return {"products" : products }

# get  a product
@app.get("/products/{item_id}")
async def get_product(item_id : int):
    for product in products:
        if product.id == item_id:
            return {"products" : product }    
        return {"products" : "product not found" }
    
# post a product
@app.post("/products")
async def add_product (product: Product):
    products.append(product)
    return {"prompt": "Product added"}

# delete a product
@app.delete("/products/{item_id}")
async def delete_products(item_id : int):
    for product in products:
        if product.id == item_id:
            products.remove(product)
            return {"products" : "{product} removed" }    
        return {"products" : "product not found" }
    
# update a product
@app.put("/products/{item_id}")
async def update_products(item_id : int, item: str, price: float):
    for product in products:
        if product.id == item_id:
            product.item = item
            product.price = price
            
            return {"products" : product }    
        return {"products" : "product not found" }




# the codes below demonstrate the use of async and await
# and how it is different from the normal function
async def fetch(url):
    print (f"fetching {url}")
    await asyncio.sleep(5)
    print (f"done fetching {url}")
    
async def main():
    await asyncio.gather(
        fetch("https://example.com1"),
        fetch("https://example.com2"),
        fetch("https://example.com3"),
        fetch("https://example.com4"),
    )
if __name__ == "__main__":
    asyncio.run(main())
    
def get(url):
    print (f"fetching {url}")
    sleep(5)
    print (f"done fetching {url}")

def getmain():
    get("https://get.com1")
    get("https://get.com2")
    get("https://get.com3")
    get("https://get.com4")

if __name__ == "__main__":
    getmain()