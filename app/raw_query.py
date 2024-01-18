from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None
while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastAPI',user='postgres',password='Dillu8091',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('Database Connected Successfully!')
        break
    except Exception as error:
        print('Database Not Connected')
        break

my_posts=[{"title":"First Post","content":"It's My First Post","id":1},{"title":"Second Post","content":"It's My Second Post","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
        
def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello Dilip"}

@app.get("/post")
def get_post(db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # my_posts=cursor.fetchall()
    data=db.query(models.Post).all()
    return {"data": data,"message":"Post listing","status":status.HTTP_200_OK}

@app.post("/create_post",status_code=status.HTTP_201_CREATED)
def create_post(payLoad:Post):
    # post_dict=payLoad.dict()
    # post_dict['id']=randrange(0,100000)
    # my_posts.append(post_dict)
    cursor.execute(""" INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING * """,(payLoad.title,payLoad.content))
    record=cursor.fetchone()
    conn.commit()
    return {"data": record,"message":"Record Created Successfully!"}

@app.get("/posts/{id}")
def get_post_by_id(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with Id {id} Record Not Found!")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"Post with Id {id} Record Not Found!"}
    return {"post_details":post}


@app.delete("/posts/{id}")
def delete_post_by_id(id:int):
    cursor.execute("""DELETE from posts where id= %s returning *""",(str(id)))
    record=cursor.fetchone()
    conn.commit()
    if record==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Record Not Exits")
    return {"record":record,"message":"Record Deleted Successfully!","status":status.HTTP_204_NO_CONTENT}
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_post_by_id(id:int,payload:Post):
    cursor.execute("""UPDATE posts set title=%s,content=%s WHERE id=%s RETURNING * """,(payload.title,payload.content,str(id)))
    record=cursor.fetchone()
    conn.commit()
    if record==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Record Not Exits")
    return {"data":record,"message":"Record Updated Successfully!"}
