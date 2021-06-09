from fastapi import FastAPI, Header, Depends, HTTPException
from models.user import User
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, check_jwt_token, create_jwt_token
from models.jwt_user import JWTUser

app_v2 = FastAPI(root_path="/v2")

# Python will change de - to _ in request.
@app_v2.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header("Ahora si me ves!"), jwt: bool = Depends(check_jwt_token)):
    return {"request body" : user, "request custom x-header": x_custom}

@app_v2.post("/token")
async def login_for_acces_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {
        "username": form_data.username,
        "password": form_data.password
    }
    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)
    
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return {"token": jwt_token}
