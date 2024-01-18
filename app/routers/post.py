from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from .. import models,schemas,utils,oauth2
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Post']
)

# @router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.PostVoteResponse])
@router.get("/",response_model=List[schemas.PostVoteResponse])
def get_post(db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user),limit:int=10,search:Optional[str]=""):
    data = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).filter(models.Post.user_id==get_current_user.id).filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).all()
    # data = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    return data


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_post(payLoad: schemas.CreatePost, db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    record = models.Post(user_id=get_current_user.id,**payLoad.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post_by_id(id: int, db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id {id} Record Not Found!",
        )
    return  post


@router.delete("/{id}")
def delete_post_by_id(id: int, db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    record = db.query(models.Post).filter(models.Post.id == id)
    post=record.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Exits"
        )
    if post.user_id!=get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This User Don't Have Access to delete this post"
        )
    record.delete(synchronize_session=False)
    db.commit()
    return {
        "record": record,
        "message": "Record Deleted Successfully!",
        "status": status.HTTP_204_NO_CONTENT,
    }


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED
)
def update_post_by_id(id: int, payload: schemas.Post, db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    record = query.first()
    if record == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record Not Exits"
        )
    query.update(
        {"title": payload.title, "content": payload.content}, synchronize_session=False
    )
    db.commit()
    return {"data": query.first(), "message": "Record Updated Successfully!"}