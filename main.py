from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage
import os


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

    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg["Subject"] = f"New Portfolio Message from {message.name}"
    msg["From"] = email_user
    msg["To"] = email_user

    msg.set_content (
        f"""
Name: {message.name}
Email: {message.email}

Message:
    {message.message}
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

    return {"status": "success"}
