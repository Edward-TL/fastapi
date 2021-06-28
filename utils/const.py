# Created by passing in terminal: openssl rand -hex 32
JWT_SECRET_KEY = "34e7c0cbcda110dba3fdbf2192b6028d02ba6ac64361f0a688fb145a9454bde8"
JWT_ALGORITHM = "HS256"
# One mont of expiration = minutes_hour * hours_day * n_days
JWT_EXPIRATION_TIME_MINUTES =  60 * 24 * 30

# DESCRIPTIONS FOR DOCUMENTATION
API_DESCRIPTION = f"""It's done from an Udemy's course: Complete Backend (API) Development with Python A-Z

Teacher: Mehmet Nuri Yumuşak

Made by: Edward TL
"""
API_TITLE = "Bookstore from Udemy's course"
DESCRIPTION_TOKEN = "It checks the username and pasword. If they are true, it returns JWT token to you"
ISBN_DESCRIPTION = "It is an unique identifier for books"

# DATABASE
DB_HOST = "165.232.142.214"
DB_USER = "admin"
DB_PASSWORD = "secret_password123"
DB_NAME = "bookstore"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

UPLOAD_PHOTO_APIKEY = "d394465f8ceddab5768cbdc533549c39"
UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?key={UPLOAD_PHOTO_APIKEY}"