from fastapi import FastAPI

app = FastAPI(title="HR Assistant API")

@app.get("/")
def health():
    return {"status": "HR Assistant API is running"}