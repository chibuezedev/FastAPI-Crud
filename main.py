from http.client import HTTPException
from typing import Optional

from sqlalchemy.orm import Session
from mimetypes import init
from fastapi import FastAPI, status
from database import Base, Post, DATABASE_URL
from datatype import PostRequest
from sqlalchemy.orm import sessionmaker
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine


# Create a sqlite engine instance
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


recreate_database()

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Welcome To Wodoo!"}

@app.post('/post')
async def create(post: PostRequest):

    session = Session()
    
    new_post = Post(
        title=post.title,
        description=post.description,
        createdBy=post.createdBy,
        category=post.category
    )

    session.add(new_post)
    session.commit()
    session.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": "success"}
    )

@app.get('/post/{id}')
def read_a_post(id: int):
    session = Session()
    
    post = session.query(Post).filter(Post.id == id).first()
    session.close()
    
    result = jsonable_encoder({"post": post})
    
    return JSONResponse(
        status_code=200, content={"message": "success", "post": result}
    )

@app.get('/post')
def all_posts(page_limit: int = 10, page: int = 1):
    if page_limit > 100 or page_limit < 0:
        page_limit = 100
    
    session = Session()
    
    posts = session.query(Post).limit(page_limit).offset((page - 1) * page_limit).all()
    session.close()
    
    result = jsonable_encoder({"posts": posts})
    
    return JSONResponse(
        status_code=200, content={"message": "success", "posts": result}
    )

@app.put('/post/{id}')
def update_post(id: int, title: Optional[str] = None, description: Optional[str] = None):
    try:
        
        session = Session()
        post = session.query(Post).get(id)
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

        if title is not None:
            post.title = title
        if description is not None:
            post.description = description
        
        session.commit()
        
        updatedPost = jsonable_encoder({"post": post})

        return JSONResponse(
            status_code=200, content={"message": "success", "updated_post": updatedPost}
        )
    except Exception as e:
        session.rollback()  # Rollback changes if an exception occurs
        raise(e)
    finally:
        session.close()
        
        
@app.delete('/post/{id}')
def delete_a_post(id: int):
    
    session = Session()
    post = session.query(Post).get(id)
    session.delete(post)
    
    session.commit()
    session.close()
    
    return JSONResponse(
        status_code=200, content={"message": "success"}
    )


@app.exception_handler(Exception)
def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(
        status_code=status_code,
        content={"status_code": status_code, "message": message},
    )