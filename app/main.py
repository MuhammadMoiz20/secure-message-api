from fastapi import FastAPI

from .db import Base, engine
from .routes import auth as auth_routes, messages as messages_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="secure-message-api")
app.include_router(auth_routes.router)
app.include_router(messages_routes.router)


@app.get("/")
def root():
    return {"status": "ok"}
