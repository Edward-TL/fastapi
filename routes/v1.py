from fastapi import FastAPI, Body, Header, File, APIRouter
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response 
from utils.helper_functions import upload_image_to_server
from utils.db_functions import (db_check_personel, db_get_book_with_isbn,
                                    db_get_author,db_get_author_from_id, db_patch_author_name)

app_v1 = APIRouter()

@app_v1.post("/login", tags=['user'])
async def get_user_validation(username:str=Body(...), password:str = Body(...)):
    result = await db_check_personel(username, password)
    if result:
        return {"is_valid": True, "body": result}
    else:
        return Response(headers={"is_valid":"False"}, status_code=HTTP_401_UNAUTHORIZED)

# Returning an object
# Without author: response_model_exclude=['author']
# Only this params: response_model_include=['name', 'year']
@app_v1.get("/book/{isbn}", response_model = Book, response_model_include=['name', 'year'])
async def get_book_with_isbn(isbn:str):
    # Gets the book object with author's name but not author as an object
    book = await db_get_book_with_isbn(isbn)

    # Needs the author object because of book model
    author = await db_get_author(book["author"])
    author_obj = Author(**author)
    book["author"] = author_obj

    # Having the book object, with the author object inside, now
    # it runs perfectly
    result_book = Book(**book)
    
    # You cannot pass objetcs on a dictionary
    return result_book

@app_v1.get("/author/{id}/book")
async def get_authors_book(id: int, order: str = "asc"):
    author = await db_get_author_from_id(id)
    if author is not None:
        books = author['books']
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)
        return {"books": books}
    else:
        return {"result": "No author with corresponding id"}

@app_v1.patch("/author/{id}/name")
async def patch_author_name(id:int, name: str = Body(..., embed=True)):
    await db_patch_author_name(id, name)
    return {"result": "name is updated"}

@app_v1.post("/user/author")
async def post_user_and_author(user: User, author: Author,
                                bookstore_name: str = Body(..., embed=True)):
    return {
        "json_user": user,
        "json_author" : author,
        "json_bookstore_name" : bookstore_name
        }

# Receive Files
@app_v1.post("/user/photo")
async def upload_user_photo(response:Response, profile_photo: bytes = File(...)):
    await upload_image_to_server(profile_photo)
    return {"file size": len(profile_photo)}