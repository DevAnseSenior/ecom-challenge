import uvicorn
from fastapi import FastAPI

from shared.database import engine, Base
from category.routers import category_router

from category.models.category_model import Category

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def oi_eu_sou_programador() -> str:
    return "Teste!"


app.include_router(category_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
