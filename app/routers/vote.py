from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils,oauth2

router=APIRouter(
    prefix='/votes',
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(payLoad: schemas.Vote,db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    record = db.query(models.Post).filter(models.Post.id == payLoad.post_id)
    post=record.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Exits"
        )
    query=db.query(models.Vote).filter(models.Vote.post_id == payLoad.post_id,models.Vote.user_id == get_current_user.id)
    record_found=query.first()
    if(payLoad.dir==1):
            if record_found:
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Already Voted this Post",
            )
            new_vote=models.Vote(post_id=payLoad.post_id,user_id=get_current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message":"Vote Added successfully","status":status.HTTP_201_CREATED}
    else:
            query.delete(synchronize_session=False)
            db.commit()
            return {"message":"Vote Deleted successfully","status":status.HTTP_200_OK}
    