from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/api/hello")
async def root():
    return {"message": "Hello World"}