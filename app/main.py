from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health_check import router as health_check_router

from app.api.telegram import router as telegram_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #await monitor.start_client()
    yield
    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)
app.include_router(health_check_router, prefix='')
app.include_router(telegram_router, prefix='/telegram')
