import uvicorn
from fastapi import FastAPI

from app.routers import category_router, product_router, user_router, user_vs_products_router
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "The app is running"}


app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(user_router.router)
app.include_router(user_vs_products_router.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
