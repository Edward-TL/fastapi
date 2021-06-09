from datetime import datetime

from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.jwt_user import JWTUser
from routes.v1 import app_v1
from routes.v2 import app_v2
from utils.security import authenticate_user, check_jwt_token, create_jwt_token
from utils.const import API_DESCRIPTION, API_TITLE, DESCRIPTION_TOKEN

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version="1.0.0")

app.include_router(app_v1, prefix="/v1", dependencies= [Depends(check_jwt_token)])
app.include_router(app_v2, prefix="/v2", dependencies= [Depends(check_jwt_token)])

@app.post("/token", description=DESCRIPTION_TOKEN, summary="Returns the JWT token")
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
    return {"access_token": jwt_token}


@app.middleware("http")
async def middleware(request: Request, call_next):
    # Modify request
    start_time = datetime.utcnow()
    if not any(word in str(request.url) for word in ["/token", "/docs", "/openapi.json"]):
        # Not all headers hace "Authorization" key
        try:
            jwt_token = request.headers["Authorization"].split("Bearer ")[1]
            # It's more readable "if not valid", than "if not is_valid"
            valid = check_jwt_token(jwt_token)
        except Exception as e:
            valid = False

        if not valid:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)


    # Modify response   
    response = await call_next(request)
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response
