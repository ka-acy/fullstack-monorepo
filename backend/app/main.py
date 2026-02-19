from fastapi import FastAPI

app = FastAPI(title="Backend API")


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/ping")
def ping():
    return {"message": "pong"}
