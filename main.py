# Init FastAPI

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

# Import routers in modules

from routes import block, connection, container, design, group, history, link

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

app.include_router(block.router)
app.include_router(connection.router)
app.include_router(container.router)
app.include_router(design.router)
app.include_router(group.router)
app.include_router(history.router)
app.include_router(link.router)

# Run with uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)