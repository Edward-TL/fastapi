# Created by passing in terminal: openssl rand -hex 32
JWT_SECRET_KEY = "34e7c0cbcda110dba3fdbf2192b6028d02ba6ac64361f0a688fb145a9454bde8"
JWT_ALGORITHM = "HS256"
# One mont of expiration = minutes_hour * hours_day * n_days
JWT_EXPIRATION_TIME_MINUTES =  60 * 24 * 30