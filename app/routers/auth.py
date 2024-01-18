from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models,schemas,utils,oauth2

router=APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(payLoad: OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    record = db.query(models.User).filter(models.User.email == payLoad.username).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials",
        )
    if not utils.verify_password(payLoad.password,record.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials",
        )
    access_token=oauth2.create_access_token(data={"user_id":record.id})
    return  {"token":access_token,"token_type":'bearer'}