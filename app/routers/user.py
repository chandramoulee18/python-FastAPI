from .. import model,schema,util
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model= schema.UserOut)
def createUser(user: schema.CreateUser,db:Session = Depends(get_db)):

    hashedPassword = util.hash_password(user.password)
    user.password = hashedPassword
    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}",response_model= schema.UserOut)
def getUser(id:int,db:Session = Depends(get_db)):
    singleUser = db.query(model.User).get(id)
    print(singleUser)
    if singleUser==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" NO user is present with id==>{id}")
    return singleUser