from fastapi import FastAPI
import cloudinary
import os
from routes.users import users_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://trust-bank-vera.netlify.app",
    "https://trust-bank-vera.netlify.app/",
]



cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET"),
    )

app = FastAPI(title="Trust Bank API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Trust Bank API"
    }

app.include_router(users_router)

