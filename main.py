# Init FastAPI

import uvicorn
from fastapi import FastAPI

app = FastAPI()

# Import routers in modules

from routes import block, connection, container, design, history, link

app.include_router(block.router)
app.include_router(connection.router)
app.include_router(container.router)
app.include_router(design.router)
app.include_router(history.router)
app.include_router(link.router)

# Run with uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)