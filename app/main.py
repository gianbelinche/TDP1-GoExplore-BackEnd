import os
import uvicorn
from fastapi import FastAPI
from app.api.ping import router as ping_router

from app.config.logger import setup_logger
from fastapi.middleware.cors import CORSMiddleware

# Setup logger
logger = setup_logger(name=__name__)

# Create app with FAST API
app = FastAPI(debug=True)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(ping_router, prefix="/api")

if __name__ == "__main__":
    port = os.environ.get('PORT', 8080)
    logger.info("Using port: " + port)
    uvicorn.run(app, host='0.0.0.0', port=port)
