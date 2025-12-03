from fastapi import FastAPI

app = FastAPI(title="MOA API")

@app.get("/")
def root():
    return {"message": "API do MOA funcionando!"}
