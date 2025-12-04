from fastapi import APIRouter, Form
from db import users_collection
from fastapi import HTTPException, status
from pydantic import EmailStr
from typing import Annotated
import bcrypt
import os
import jwt
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId
from utils import replace_user_id, valid_id


users_router = APIRouter(tags=["Users"])

@users_router.post("/users/signup")
def register_user(
        email: Annotated[EmailStr, Form()],
        password: Annotated[str, Form(min_length=8)]):

    user_count = users_collection.count_documents({"email": email})
    if user_count > 0:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists!")


    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())


    user_created = {
        "email": email,
        "password": hash_password,
    }

    registered_user = users_collection.insert_one(user_created)

    return {
        "message": "Signup successful",
        "user_id": str(registered_user.inserted_id)
    }

@users_router.post("/users/login")
def login_user(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)]
):
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found!")

    correct_password = bcrypt.checkpw(password.encode(), user["password"])
    if not correct_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong credentials!")


    encoded_jwt = jwt.encode({
            "id": str(user["_id"]),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60)
        }, os.getenv("JWT_SECRET_KEY"), os.getenv("JWT_ALGORITHM"))

    return {
        "message": "Login successful",
        "access_token": encoded_jwt
    }

@users_router.get("/users")
def get_users():
    all_users = users_collection.find().to_list()
    return {"users": list(map(replace_user_id, all_users))}


@users_router.get("/users/{user_id}")
def get_user_by_id(user_id):
    valid_id(user_id)
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return {"data": replace_user_id(user)}


@users_router.delete("/users/{user_id}")
def delete_user(user_id):
    valid_id(user_id)
    # Delete user from database
    delete_result = users_collection.delete_one(
        filter={"_id": ObjectId(user_id)})
    if not delete_result:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received")

    return {"message": f"user with id {user_id} has been deleted successfully."}