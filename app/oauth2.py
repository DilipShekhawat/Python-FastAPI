from fastapi import FastAPI, Response, status, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import schemas,database,models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_time

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,exception):
     try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id=payload.get('user_id')
        if id is None:
            raise exception
        token_data = schemas.TokenData(id=id)
     except JWTError:
            raise exception
     return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
     exception=HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Could not validate credentials",
          headers={"WWW-Authenticate": "Bearer"}
     )
     UserId=verify_access_token(token,exception)
     return db.query(models.User).filter(models.User.id == UserId.id).first()
