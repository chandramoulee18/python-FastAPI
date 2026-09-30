from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schema,database,model
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt =jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credentails_exception):
    # print(f"############# Entering verify_access_token ##############")
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        print(payload)
        id:str = payload.get("user_id")

        # print(f"############# Entering verify_access_token ##############")

        # print(id)

        if id is None:
            raise credentails_exception
        # print(f"############# Entering verify_access_token : Before Token data ##############")
        token_data = schema.TokenData(id=str(id))
        # print(f"############# Entering verify_access_token : Token data ##############")
        # print(token_data)
    except JWTError as e:
        # print(f"############# Entering verify_access_token:Exception Block ##############")
        # print(e)
        raise credentails_exception
    except ArithmeticError as e:
        # print(f"############# Entering verify_access_token:ArithmeticError Exception Block ##############")
        # print(e)
        raise credentails_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db : Session = Depends(database.get_db)):
    # print(f"############# Entering get_current_user ##############")
    credentails_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token,credentails_exception)

    singleUser = db.query(model.User).get(token.id)

    print(singleUser)

    return singleUser

