import uvicorn
from fastapi import FastAPI

from category.routers import category_router

app = FastAPI()

@app.get("/")
def oi_eu_sou_programador() -> str:
    return "Teste!"

app.include_router(category_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
