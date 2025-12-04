from bson.objectid import ObjectId
from fastapi import HTTPException, status


def replace_user_id(user):
    user["id"] = str(user["_id"])
    del user["_id"]
    return user

def valid_id(id):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id received"
        )