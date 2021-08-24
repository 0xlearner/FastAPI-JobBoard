from fastapi import APIRouter, HTTPException, status, Request
from fastapi import Depends
from jose import jwt

from db.models.users import User
from schemas.users import UserCreate, ShowUser
from db.repository.users_data_access_layer import Users
from core.auth import Auth
from core.mailer import Mailer
from core.config import Settings
from depends import get_user_db
from db.repository.users_data_access_layer import Users
from core.auth import Auth

router = APIRouter()

get_settings = Settings()

@router.post("/signup")
async def create_user(form_data: UserCreate = Depends(), users: Users = Depends(get_user_db)):
    # CHECK IF USER ALREADY EXISTS
    if await users.get_user_by_email(email=form_data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    # CHECK IF USERNAME ALREADY EXISTS
    elif await users.get_user_by_username(username=form_data.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # CREATE USER WITH USERS METHOD
    # now the hashing of the password is done directly in the creation method
    new_user = await users.create_user(form_data)
    
    # GET TOKEN
    # we no longer create a new uid for JTI, but use the one created automatically during user creation
    # so I modified the get_confirmation_token function so that it takes the user's JTI uid as a parameter
    confirmation_token = Auth.get_confirmation_token(
                            new_user.email,
                            new_user.confirmation)

    # SEND AN EMAIL WITH TOKEN
    try:
        Mailer.send_confirmation_message(
            confirmation_token["token"], form_data.email)
    except ConnectionRefusedError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email couldn't be send. Please try again."
        )
    # RETURN USER
    return {"res": "created"}

@router.get("/verify/{token}", response_model=ShowUser)
async def verify(token: str, users: Users = Depends(get_user_db)):
    invalid_token_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token")
    
    # TRYING DECODE TOKEN
    try:
        payload = jwt.decode(token, get_settings.SECRET_KEY, algorithms=[
                             get_settings.TOKEN_ALGORITHM])
    except jwt.JWSError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token has Expired")
        
    # CHECK IF THE SCOPE IS OK
    if payload['scope'] != 'registration':
        raise invalid_token_error
    
    # TRY TO GET AN USER WITH THE ID FROM TOKEN
    user = await users.get_user_by_email(email=payload['sub'])
    print(payload['jti'])
    #print(user.confirmation)
    
    # CHECK IF WE FOUND AN USER AND IF THE UID CONFIRMATION IS THE SAME OF THE TOKEN
    if not user or str(user.confirmation) != payload['jti']:
        raise invalid_token_error
    
    # CHECK IF THE USER IS ALREADY ACTIVE
    if user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User already Activated")
        
    # IF ALL IT'S OK, WE UPDATE THE CONFIRMATION AND IS_ACTIVE ATTRIBUTE AND CALL THE SAVE METHOD
    user.confirmation = None
    user.is_active = True
    await users.save(user)
    return {"res": "user created"}

@router.get("/")
async def root():
    return {"message": "Job Board"}