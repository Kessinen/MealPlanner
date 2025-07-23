from fastapi import FastAPI

from routes.meals import meal_router

app = FastAPI()

app.include_router(meal_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
