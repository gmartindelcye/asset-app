from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.asset import router as asset_router
from app.routes.owner import router as owner_router
from app.routes.user import router as user_router
from app.db import a_session

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the routers
app.include_router(asset_router, prefix="/api/assets", tags=["assets"])
app.include_router(owner_router, prefix="/api/owners", tags=["owners"])
app.include_router(user_router, prefix="/api/users", tags=["users"])

# Start the database connection
@app.on_event("startup")
async def startup():
    await a_session.connect()

# Close the database connection
@app.on_event("shutdown")
async def shutdown():
    await a_session.disconnect()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

