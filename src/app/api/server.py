from fastapi import FastAPI, HTTPException
import os
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.middleware.performance import LimitRequestSizeMiddleware

from routers import image_handler,basic

os.environ['appname'] = "image insight app"
appname = os.environ.get('appname')
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(LimitRequestSizeMiddleware)
app.include_router(image_handler.router)
app.include_router(basic.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000,reload=True,workers=1)
