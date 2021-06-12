from sqlalchemy import MetaData, create_engine, Table, Column, Integer, Text, ARRAY
from databases import Database
import asyncio

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

metadata = MetaData()
engine = create_engine(DB_URL)
metadata.create_all(engine)


books = Table(
    "books",
    metadata,
    Column("isbn", Text, primary_key=True),
    Column("name", Text),
    Column("author", Text),
    Column("year", Integer)
)

authors = Table(
    "authors",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("books", ARRAY(Text))
)

async def test_orm():
    query = authors.insert().values(id=1,name="Victor Hugo", books=["Han de Islandia", "El hombre que ríe"])
    
    await execute(query, False)

if __name__ == "__main__":


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_orm)
    