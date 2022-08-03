from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import auth, todos, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)


@app.get('/')
async def root():
    return RedirectResponse('docs')

