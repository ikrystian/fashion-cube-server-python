from fastapi import  FastAPI
from app.routers import users, products, variants, departments, categories, checkout, payment, search, filter

app = FastAPI()

app.include_router(users.router, prefix="/users")
app.include_router(products.router, prefix="/products")
app.include_router(variants.router, prefix="/variants")
app.include_router(departments.router, prefix="/departments")
app.include_router(categories.router, prefix="/categories")
app.include_router(checkout.router, prefix="/checkout")
app.include_router(payment.router, prefix="/payment/success")
app.include_router(filter.router, prefix="/filter")
app.include_router(search.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI E-commerce application!"}