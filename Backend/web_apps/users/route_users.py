from fastapi import APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Depends
from fastapi import responses
from fastapi import status
from sqlalchemy.exc import IntegrityError

from web_apps.users.forms import UserCreateForm
from db.repository.users_data_access_layer import Users
from schemas.users import UserCreate
from depends import get_user_db
from core.auth import Auth
from core.mailer import Mailer


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("users/register.html", 
    {"request": request})

@router.post("/register/")
async def register_user(request: Request, user_reg: Users = Depends(get_user_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(username=form.username, email=form.email, password=form.password)
        try:
            user = await user_reg.create_user(user=user)
            confirmation_token = Auth.get_confirmation_token(
                            user.email,
                            user.confirmation)

            # SEND AN EMAIL WITH TOKEN
            try:
                Mailer.send_confirmation_message(
                    confirmation_token["token"], form.email)
            except ConnectionRefusedError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Email couldn't be send. Please try again."
                )
            return {f"Hello {user.username}, thanks for choosing our services. Please check your email to activate your account."}

        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__) 