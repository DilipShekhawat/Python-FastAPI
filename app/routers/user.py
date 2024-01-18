from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils
from sqlalchemy.exc import IntegrityError

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(payLoad: schemas.CreateUser, db: Session = Depends(get_db)):
    try:
        payLoad.password = utils.hash(payLoad.password)
        record = models.User(**payLoad.dict())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError as e:
        # Check if the error is a unique violation error
        if "unique constraint" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already exists")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with Id {id} Record Not Found!",
        )
    return user