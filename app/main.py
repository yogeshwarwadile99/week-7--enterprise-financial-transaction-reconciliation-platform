from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from app.config import config
from app.database import Base, engine
from app.middleware.error_handler import global_exception_handler, app_exception_handler, AppException
from app.routes import auth, accounts, transactions, reconciliation, risk, audit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(reconciliation.router)
app.include_router(risk.router)
app.include_router(audit.router)

@app.get("/")
async def root():
    return {"name": config.APP_NAME, "version": config.APP_VERSION, "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": config.APP_NAME, "version": config.APP_VERSION}

@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 {config.APP_NAME} v{config.APP_VERSION} started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Application shutting down...")
