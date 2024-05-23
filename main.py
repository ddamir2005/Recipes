import time

from fastapi.security.utils import get_authorization_scheme_param

from apis.base import api_router
from apis.version1.route_login import get_current_user_from_token
from core.config import settings
from db.base import Base
from db.models.users import User
from db.session import engine
from db.utils import check_db_connected
from db.utils import check_db_disconnected
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from webapps.base import api_router as web_app_router
from sqlalchemy.orm import Session

def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    try:
        token = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        with Session(engine) as db:
            current_user: User = get_current_user_from_token(token=param, db=db)
    except HTTPException as e:
        current_user = None
    except Exception as e:
        current_user = None
    request.app.state.current_user = str(current_user.id if current_user else "")
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Current-User"] = str(current_user.id if current_user else "")
    return response

@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
