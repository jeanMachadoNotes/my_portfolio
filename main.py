from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class ContactMessage(BaseModel):
    name: str
    email: str
    message: str

app = FastAPI()

# allow React to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #TEMP: allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/home")
def home():
    return {
        "title": "Welcome",
        "message": "This content came from the Python backend. This is an endpoints data."
    }

@app.get("/api/services")
def services():
    return {
        "services": [
            "Web development",
            "Python automation",
            "Backend APIs"
        ]
    }


@app.get("/api/contact")
def contact():
    return {
        "email": "jeanmachadotx@gmail.com"
    }

@app.post("/api/contact")
def contact(message: ContactMessage):
    print("New contact message:")
    print(message)

    return {"status": "success"}
