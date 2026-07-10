import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI
from apps.routers.auth import router as auth_router
from apps.config import OPENAI_API_KEY
from apps.background.monitor import monitor_prices
from apps.database import Base, engine
from apps.models import TradeSignalDB  # noqa: F401

from apps.routers.signals import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not OPENAI_API_KEY:
        print("WARNING: OPENAI_API_KEY not found")
    else:
        print("API keys loaded successfully")

    Base.metadata.create_all(bind=engine)

    # Start background monitoring loop
    task = asyncio.create_task(monitor_prices())
    print("Price monitoring started")
    yield
    # Stop the task when server shuts down
    task.cancel()
    print("Price monitoring stopped")
    
app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(auth_router)
