from fastapi import FastAPI
from oracle.routes import router as oracle_router

app = FastAPI(title="AI Climate Oracle")
app.include_router(oracle_router)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Climate Oracle powered by Bittensor!"}
