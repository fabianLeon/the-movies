import jwt
import datetime

secret_key = "prueba"
 
def tokenApi(payload):
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
 