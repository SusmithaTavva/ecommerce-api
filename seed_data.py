from app.database import get_database, get_products_collection, get_orders_collection
from bson.objectid import ObjectId

db = get_database()
products = get_products_collection()
orders = get_orders_collection()

# Insert Products
products.insert_many([
    {"name": "string", "price": 100.0, "sizes": [{"size": "string", "quantity": 0}]},
    {"name": "Sample", "price": 100.0},
    {"name": "Sample 2", "price": 10.0}
])

# Insert Orders
orders.insert_many([
    {"userId": "user_1", "items": [{"productId": "123456789", "qty": 3}, {"productId": "222222", "qty": 3}]}
])