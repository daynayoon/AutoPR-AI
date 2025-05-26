# main.py creates the FastAPI app (entrypoint)
# register routers, add middleware, load settings

from fastapi import FastAPI
from app.routers import github, review
from app.core.config import settings
from app.core.exception_handler import validation_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

# set the routers (sub fastapi application, path operations)
app.include_router(github.router, prefix="/github", tags=["Github"])
app.include_router(review.router, prefix="/review", tags=["Code Review"])

# custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# root entrypoint
@app.get("/")
async def root():
    return {"message": "Hello, AutoPR-AI is up and running"}

# load settings
@app.on_event("startup")
async def startup_event():
    print("server started") # e.g., MongoDB connected, load variables, init

@app.on_event("shutdown")
async def shutdown_event():
    print("server shutdown")