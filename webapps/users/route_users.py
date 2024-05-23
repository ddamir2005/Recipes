from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.users import create_new_user
from db.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from fastapi.security.utils import get_authorization_scheme_param
from db.repository.users import get_user_by_id
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from webapps.users.forms import UserCreateForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)

@router.get("/user")
def recipe_detail(request: Request, db: Session = Depends(get_db)):
    current_user_id = request.app.state.current_user
    user = get_user_by_id(id=current_user_id, db=db)
    return templates.TemplateResponse(
        "users/detail.html", {"request": request, "user": user}
    )

@router.get("/user/{id}")
def recipe_detail(request: Request, id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(id=id, db=db)
    return templates.TemplateResponse(
        "users/detail.html", {"request": request, "user": user}
    )

@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            username=form.username, description=form.description, photo=form.photo, email=form.email, password=form.password
        )
        try:
            user = create_new_user(user=user, db=db)
            return responses.RedirectResponse(
                "/?msg=Успешная%20регистрация", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.__dict__.get("errors").append("Пользователь с таким именем или email уже существует")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)
