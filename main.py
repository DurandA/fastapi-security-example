import uvicorn
from fastapi import FastAPI

from database import create_db_and_tables
from routers import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
