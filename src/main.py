from fastapi import FastAPI
from .auth.router import router as auth_router

app = FastAPI()


@app.get('/')
def index():
    return {'Hello': 'World!'}


app.include_router(auth_router)
