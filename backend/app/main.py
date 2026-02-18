from contextlib import asynccontextmanager
from .db.neo4j_driver import neo4j_driver

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Verify connections
    logger.info("🚀 System Startup: Verifying connections...")
    try:
        neo4j_driver.verify_connectivity()
        logger.info("✅ Neo4j Connected")
    except Exception as e:
        logger.warning(f"⚠️ Neo4j Connection Failed: {e}")
    
    yield
    
    # Shutdown: Close connections
    logger.info("🛑 System Shutdown: Closing connections...")
    neo4j_driver.close()
    logger.info("✅ Neo4j Driver Closed")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=None,
    lifespan=lifespan
)

# Enable Prometheus Metrics
Instrumentator().instrument(app).expose(app)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(Exception, global_exception_handler)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Configure CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def root():
    return {"message": "Welcome to EcoTwin API", "status": "healthy"}

# Include routers
app.include_router(activities.router, prefix=settings.API_V1_STR + "/activities", tags=["activities"])
app.include_router(batch.router, prefix=settings.API_V1_STR + "/batch", tags=["batch"])
app.include_router(analytics.router, prefix=settings.API_V1_STR + "/analytics", tags=["analytics"])
app.include_router(health.router, tags=["health"])
