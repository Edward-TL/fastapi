from fastapi import FastAPI, Body, Header, File
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response 

app_v1 = FastAPI(root_path="/v1")

@app_v1.get("/user", tags=['user'])
async def get_user_validation(password:str):
    return {"query parameter": password}

# Returning an object
# Without author: response_model_exclude=['author']
# Only this params: response_model_include=['name', 'year']
@app_v1.get("/book/{isbn}", response_model = Book,
    response_model_include=['name', 'year'])
async def get_book_with_isbn(isbn:str):
    # First, we need and Author object
    author_dict = {
        "name" : "Gabo",
        "book" : ["Primer libro", "La continuacion"]
    }
    author1 = Author(**author_dict)

    book_dict = {
        "isbn" : isbn,
        "name" : "El mejor libro de todos los tiempos",
        "year" : 2019,
        "author" : author1
    }
    book1 = Book(**book_dict)
    
    # You cannot pass objetcs on a dictionary
    return book1

@app_v1.get("/author/{id}/book")
async def get_authors_book(id: int, category: str, order: str = "asc"):
    return {"query changable parameter": order + category + str(id)}

@app_v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {'name in json_body' : name}

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
    response.headers['x-file-size'] = "El archivo pesa: " + str(len(profile_photo)) + " bytes"
    response.set_cookie(key="cookie-api", value='test')
    return {"file size": len(profile_photo)}