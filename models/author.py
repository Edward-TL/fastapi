from pydantic import BaseModel
from typing import List

# from models.book import Book
# Originally use, but replace by isbn at books list

class Author(BaseModel):
    name: str
    books: List[str]