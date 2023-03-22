# Init FastAPI

import uvicorn
from fastapi import FastAPI

app = FastAPI()

# Import routers in modules

from routes import block

app.include_router(block.router)

# Run with uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)