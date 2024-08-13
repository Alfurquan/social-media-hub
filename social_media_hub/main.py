from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from .routers import user, auth, post

app = FastAPI(
    title="Social media hub",
    description="Small rest api app for social media",
    version="v1"
)
app.include_router(user.router_v1, prefix= '/api/v1/users')
app.include_router(auth.router)
app.include_router(post.router_v1,  prefix= '/api/v1/posts')

parent_dir_path = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(parent_dir_path, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def root():
    return {"message": "Hello from post app"}


def main():
    """
    Launch web server
    """
    uvicorn.run("social_media_hub.main:app", host="127.0.0.1", port=8000, reload=True)