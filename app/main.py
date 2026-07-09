from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.items import router as items_router
from app.db.database import Base, engine
from app.db import models_orm  # noqa: F401  (registra el modelo en Base.metadata)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Items API", version="1.0.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


app.include_router(items_router)
