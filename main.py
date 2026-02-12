from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
import smtplib
from email.message import EmailMessage
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


class ContactMessage(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(min_length=10, max_length=2000)
    company: str | None = None

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# allow React front end to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jeanmachado.net", "https://www.jeanmachado.net"], #only this can call Python backend
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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


@app.post("/api/contact")
@limiter.limit("5/minute")
def contact(request: Request, message: ContactMessage):

    try:
        # Honeypot check
        if hasattr(message, "company") and message.company:
            return {"status": "blocked"}

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
    
    except Exception:
        return {"status":"error"}

