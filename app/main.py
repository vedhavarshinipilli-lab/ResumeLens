from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routers.predict import router as predict_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows requests from any frontend
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(predict_router)

@app.get("/")
def root():
    return {"status": "server is running"}
# server entry point
# uvicorn main:app --reload