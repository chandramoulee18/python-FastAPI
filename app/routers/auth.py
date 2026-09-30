from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schema,model,util,oAuth2


router = APIRouter(
      tags=['Authentication']
)

@router.post("/login",response_model=schema.Token)
#def login(userCredentials:schema.UserLogin,db : Session = Depends(database.get_db)):
def login(userCredentials:OAuth2PasswordRequestForm = Depends(),db : Session = Depends(database.get_db)):
    #user = db.query(model.User).filter(model.User.email == userCredentials.email).first()
    user = db.query(model.User).filter(model.User.email == userCredentials.username).first()
    #print(singleUser)
    if not user or not util.verify_password(userCredentials.password,user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")

    access_token = oAuth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}