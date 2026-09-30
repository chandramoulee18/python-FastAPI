from fastapi import FastAPI, Depends
from fastapi.params import Body
from random import randrange
from psycopg2.extras import RealDictCursor
from . import model
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# the following line is not needed if you use alembic
# model.Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(settings.database_hostname)


my_posts = [{"title": " This is the title of my 1st Post", "content": " This is the Content of my 1st Post", "id": "1"},
            {"title": " This is the title of my 2nd Post", "content": " This is the Content of my 2nd Post", "id": "2"}]


def findPost(id):
    for p in my_posts:
        if int(p["id"]) == id:
            print("in findPost..... ")
            return p


def findPostIndex(id):
    for i, p in enumerate(my_posts):
        if int(p["id"]) == id:
            return i


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(model.Post)
    print(posts)
    return {"Data": "successful query"}


@app.get("/")
async def root():
    return {"message": "Hello Mr. Kian Mukherjee!!!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
