from contextlib import asynccontextmanager
from fastapi import FastAPI
from Backend.app.core.configure import settings
from Backend.app.core.logging import setup_logging,get_logger
from Backend.app.routers.api_router.api_routers import api_router


setup_logging()

# setting the logger
logger=get_logger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    Application lifecycle manager.

    Startup:
        Initialize resources required by the application.

    Shutdown:
        Gracefully release resources before exiting.
    """
    logger.info("Application is started......")
    
    yield
    
    logger.info("Application is shutdowned.........")
app=FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    )

app.include_router(api_router)

