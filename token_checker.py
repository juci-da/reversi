import os
import hashlib

user_tokens=["","",""]
def ramdom_token()-> str:
    return hashlib.sha256(os.urandom(64)).hexdigest()
def get_token(who:int)->str:
    return user_tokens[who]
def check_token(who:int,token:str)->bool:
    if 1<=who<=2:
        return user_tokens[who]==token
    return False
def reset_tokens():
    global user_tokens
    user_tokens=["",ramdom_token(),ramdom_token()]