from fastapi import FastAPI
from app.models.models_product import Product

app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

# http://127.0.0.1:8000/product/123
@app.get("/product/{product_id}")
def func_product(product_id: int) -> Product:
    for product in sample_products:
        if product['product_id'] == product_id:
            return product
        return {"error": "not found product with product_id"}


# http://127.0.0.1:8000/products/search?keyword=phone&category=Electronics&limit=5
@app.get("/products/search")
def func_product_search(keyword: str, category: str = None, limit: int = 10):
    products = []
    for product in sample_products:
        if keyword.lower() in product['name'].lower() and (category.lower() in product['category'].lower()):
            products.append(product)
    return products[:limit]

