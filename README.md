E-commerce Backend API
Overview
This is a FastAPI-based backend for an e-commerce application with MongoDB integration.
Setup

Install dependencies: pip install -r requirements.txt
Set up MongoDB Atlas and update .env with MONGODB_URI.
Run the app: uvicorn app.main:app --reload

APIs

POST /products: Create a new product.
GET /products: List products with filtering and pagination.

Database

Collection: products
Fields: name, price, sizes
