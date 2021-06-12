from databases import Database
import asyncio
from orm_db import authors, books
from sqlalchemy import select

DB_HOST = "165.232.142.214"
DB_USER = "admin"
DB_PASSWORD = "secret_password123"
DB_NAME = "bookstore"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


async def connect_db():
    db = Database(DB_URL)
    await db.connect()
    return db

async def disconnect_db(db):
    await db.disconnect()

async def execute(query, is_many, values=None):
    db = await connect_db()

    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)

    await disconnect_db(db)

async def fetch(query, is_one,  values=None):
    db = await connect_db()
    
    if is_one:
        result = await db.fetch_one(query=query, values=values)
        out = dict(result)
    else:
        results = await db.fetch_all(query=query, values=values)
        out = list()
        for row in results:
            out.append(dict(row))
            
    await disconnect_db(db)

    return out

async def test_insert_orm():
    query = authors.insert().values(id=1,name="Victor Hugo", books=["Han de Islandia", "El hombre que ríe"])
    
    await execute(query, False)

async def test_where_orm():
    query = books.select().where(books.c.isbn == "isbn2")

    out = await execute(query, False)
    print(out)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete((test_where_orm()))
    # query = "INSERT INTO books VALUES(:isbn, :name, :author, :year)"
    # values1 = {
    #     "isbn": "isbn3",
    #     "name": "El psicoanalista",
    #     "author": "Jhon Katzenbach",
    #     "year": 2002
    # }

    # values2 = {
    #     "isbn": "isbn2",
    #     "name": "El señor de los anillos",
    #     "author": "J. R. R. Tolkien",
    #     "year": 1954
    # }

    # values = [values1, values2]

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete((execute(query, True, values)))

    # FETCH ONE
    query = "SELECT * FROM books WHERE isbn=:isbn"
    values = {"isbn" : "isbn1"}
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete((fetch(query, True, values))))


    # FETCH ALL METHOD
    query = "SELECT * FROM books"

    loop = asyncio.get_event_loop()
    print(loop.run_until_complete((fetch(query, False))))

    # ORM
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_orm())

    query = "SELECT * FROM authors"

    loop = asyncio.get_event_loop()
    print(loop.run_until_complete((fetch(query, False))))

    