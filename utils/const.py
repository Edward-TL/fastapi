# Created by passing in terminal: openssl rand -hex 32
JWT_SECRET_KEY = "34e7c0cbcda110dba3fdbf2192b6028d02ba6ac64361f0a688fb145a9454bde8"
JWT_ALGORITHM = "HS256"
# One mont of expiration = minutes_hour * hours_day * n_days
JWT_EXPIRATION_TIME_MINUTES =  60 * 24 * 30

API_DESCRIPTION = f"""It's done from an Udemy's course: Complete Backend (API) Development with Python A-Z

Teacher: Mehmet Nuri Yumuşak

Made by: Edward TL
"""

API_TITLE = "Bookstore from Udemy's course"

DESCRIPTION_TOKEN = "It checks the username and pasword. If they are true, it returns JWT token to you"

ISBN_DESCRIPTION = "It is an unique identifier for books"