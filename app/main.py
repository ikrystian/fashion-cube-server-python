from fastapi import  FastAPI
from app.routers import users, products, variants, departments, categories, checkout, payment, search, filter, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://example.com",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,   # Allow cookies to be sent
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allowed HTTP methods
    allow_headers=["*"],      # Allow all headers
)

app.include_router(users.router, prefix="/users")
app.include_router(products.router, prefix="/products")
app.include_router(variants.router, prefix="/variants")
app.include_router(departments.router, prefix="/departments")
app.include_router(categories.router, prefix="/categories")
app.include_router(checkout.router, prefix="/checkout")
app.include_router(payment.router, prefix="/payment")
app.include_router(filter.router, prefix="/filter")
app.include_router(search.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI E-commerce application!"}