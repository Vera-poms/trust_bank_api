from fastapi import FastAPI
import cloudinary
import os
from routes.users import users_router

cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET"),
    )

app = FastAPI(title="Trust Bank API")

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Trust Bank API"
    }

app.include_router(users_router)