import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import auth, todos, users
from config import base

settings = base.Settings()
app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)


@app.get('/')
async def root():
    return RedirectResponse('docs')


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.SERVER_IP, port=settings.SERVER_PORT, reload=True)
