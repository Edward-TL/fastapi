from fastapi import Header, APIRouter
from models.user import User
from starlette.status import HTTP_201_CREATED
from utils.db_functions import db_insert_personel

app_v2 = APIRouter()

# Python will change de - to _ in request.
@app_v2.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User):
    await db_insert_personel(user)
    return {"result": "personel is created"}