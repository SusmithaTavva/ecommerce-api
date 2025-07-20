from fastapi import FastAPI, HTTPException
from app.database import get_database, get_products_collection, get_orders_collection
from app.models import ProductCreate, ProductResponse, Size, OrderCreate, OrderResponse, OrderDetails, GetOrdersResponse
from bson import ObjectId
from typing import List, Optional

app = FastAPI()
db = get_database()
products_collection = get_products_collection()
orders_collection = get_orders_collection()

@app.post("/products")
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    if product_dict.get("sizes") is None:
        product_dict["sizes"] = []
    result = products_collection.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

@app.get("/products")
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size

    total = products_collection.count_documents(query)
    products = products_collection.find(query).skip(offset).limit(limit)
    data = [
        {
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            # Sizes are omitted as per the List Products API response example
        }
        for product in products
    ]

    page = {}
    if offset + limit < total:
        page["next"] = str(offset + limit)
    if offset > 0:
        page["previous"] = str(max(0, offset - limit))
    page["limit"] = str(limit)

    return {"data": data, "page": page}

@app.post("/orders")
async def create_order(order: OrderCreate):
    order_dict = order.dict()
    result = orders_collection.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

@app.get("/orders/{user_id}")
async def get_list_of_orders(user_id: str, limit: Optional[int] = 10, offset: Optional[int] = 0):
    query = {"userId": user_id}
    total = orders_collection.count_documents(query)
    orders = orders_collection.find(query).skip(offset).limit(limit)
    
    data = []
    total_amount = 0.0
    for order in orders:
        order_items = []
        for item in order["items"]:
            product = products_collection.find_one({"_id": ObjectId(item["productId"])})
            if product:
                order_items.append({
                    "productDetails": {"name": product["name"], "id": str(product["_id"])},
                    "qty": item["qty"]
                })
                total_amount += product["price"] * item["qty"]
        data.append({"id": str(order["_id"]), "items": order_items})

    page = {}
    if offset + limit < total:
        page["next"] = str(offset + limit)
    if offset > 0:
        page["previous"] = str(max(0, offset - limit))
    page["limit"] = str(limit)

    return {"data": data, "total": total_amount, "page": page}