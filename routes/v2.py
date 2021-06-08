from fastapi import FastAPI, Header
from models.user import User
from starlette.status import HTTP_201_CREATED

app_v2 = FastAPI(root_path="/v2")

# Python will change de - to _ in request.
@app_v2.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header("Ahora si me ves!")):
    return {"request body" : user, "request custom x-header": x_custom}