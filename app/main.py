from fastapi import FastAPI

app = FastAPI(title="secure-message-api")


@app.get("/")
def root():
    return {"status": "ok"}
