from utils.db import execute, fetch
from models.jwt_user import JWTUser

async def db_check_token_user(user:JWTUser):
    query = """SELECT *
    FROM users 
    WHERE name = :name
    """ 

    values = {
        "name": user.name
        }

    result = await fetch(query, is_one=False, values=values)
    if result is None:
        return None
    else:
        return result

async def db_check_jwt_username(username:str):
    query = """
    SELECT *
    FROM users 
    WHERE name = :name
    """
    values = {"name": username}
    
    result = await fetch(query, is_one=True, values=values)
    if result is None:
        return False
    else:
        return True

async def db_insert_personel(user):
    query = """
    INSERT INTO personel(name, password, mail, role)
    VALUES(:name, :password, :mail, :role)
    """
    values = dict(user)

    await execute(query, is_many=False, values=values)

async def db_check_personel(username, password):
    query = """SELECT *
    FROM personel 
    WHERE name = :name AND
    password = :password
    """ 

    values = {
        "name": username,
        "password": password
        }

    result = await fetch(query, is_one=True, values=values)
    if result is None:
        return False
    else:
        return result

async def db_get_book_with_isbn(isbn):
    query = """
    SELECT *
    FROM books
    WHERE isbn = :isbn
    """
    values = {"isbn": isbn}

    book = await fetch(query, True, values)
    return book

async def db_get_author(author_name):
    query = """
    SELECT *
    FROM authors
    WHERE name = :name
    """
    values = {"name": author_name}

    author = await fetch(query, True, values)
    return author

async def db_get_author_from_id(author_id):
    query = """
    SELECT *
    FROM authors
    WHERE id = :id
    """
    values = {"id": author_id}

    author = await fetch(query, True, values)
    return author

async def db_patch_author_name(id, name):
    query = """
    UPDATE authors SET name = :name WHERE id = :id
    """
    values = {
        "name": name,
        "id": id
        }
    
    await execute(query, False, values)