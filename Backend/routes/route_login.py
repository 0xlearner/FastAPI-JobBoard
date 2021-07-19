from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from jose import jwt, JWTError

from core.config import settings
from db.repository.users_data_access_layer import Users
from core.auth import Auth
from depends import get_user_db



router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
                user_session: Users = Depends(get_user_db)):

    user = await user_session.authenticate_user(form_data.username, 
                                            form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password")

    if user.is_active == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Please, activate your Account")

    access_token = Auth.get_token(data={"sub": user.username}, 
                            expires_delta=settings.USER_TOKEN_LIFETIME)

    return {"access_token": access_token, "token_type": "Bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

async def get_current_user_from_token(token: str = Depends(oauth2_scheme), user_session: Users = Depends(get_user_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate the credentials!")
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        username: str = payload.get("sub")
        print("username is", username)

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_session.get_user_by_username(username)

    if user is None:
        raise credentials_exception

    return user