from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
import time
from utils.db_functions import db_check_token_user, db_check_jwt_username

# from starlette.status import HTTP_401_UNAUTHORIZED

oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


pwd_context = CryptContext(schemes=["bcrypt"])

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


# comment also import JWTUser and fake_jwt_user 
# print(get_hashed_password("fake_password"))

# This is going to be removed until I finished the course
# jwt_user1 = {
#     "username": "user1",
#     "password": "$2b$12$1pijpPJooewNcak6ku0a0ecC2t.1Y5gdU4MazG282kNz6ee2yiSwK",
#     "disabled": False,
#     "role": "admin"
# }
# fake_jwt_user = JWTUser(**jwt_user1)

# Authenticate username and password to give JWT token
async def authenticate_user(user:JWTUser):
    # Check if there is a match in username
    potential_users = await db_check_token_user(user)
    is_valid = False
    for db_user in potential_users:
        if verify_password(user.password, db_user['password']):
            is_valid = True

    if is_valid:
        user.role = "admin"
        return user

    return None


# Create acces JWT token
def create_jwt_token(user:JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "exp": expiration
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm = JWT_ALGORITHM)

    return jwt_token

# Check whether JWT token is correct
async def check_jwt_token(token:str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        # Check if a username has it 
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")

        # Check expiration time
        if time.time() < expiration:
            # If there is a user with this username
            is_valid = await db_check_jwt_username(username)
            if is_valid:
                return final_checks(username, role)
    except Exception as e:

        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
        
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

# Last checking and returning the final result
def final_checks(username:str, role:str):
    if role == "admin":
        return True
    
    return False