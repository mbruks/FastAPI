from fastapi import FastAPI
#from app.models.models import

app = FastAPI()
all_product = {
    1: {"name": "Milk", "category": "Meal"}
}
@app.get("/product/{product_id}")
def func_product(product_id: int):
    if product_id in all_product:
        return all_product[product_id]
    return {"error: not found product with product_id"}

