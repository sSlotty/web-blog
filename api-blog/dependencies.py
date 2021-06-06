from fastapi import Header, HTTPException
from fastapi.security import OAuth2PasswordBearer


async def get_token_header(x_token: str = Header(...)):
    print(x_token)
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    print(token)
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")




