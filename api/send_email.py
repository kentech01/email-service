import os
import logging
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.middleware.cors import CORSMiddleware

from email_providers.sendgrid_provider import SendGridProvider
from email_providers.ses_provider import SESProvider

load_dotenv()

# Load allowed origins from env, comma-separated
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
# Uncomment the following lines for local development to allow all origins
# origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET")
EMAIL_PROVIDER_NAME = os.getenv("EMAIL_PROVIDER", "sendgrid")
FROM_EMAIL = os.getenv("FROM_EMAIL")

# Mapping client IDs to recipient emails
CLIENT_EMAIL_MAP = {
    "ClientA": "clientA@example.com",
    "ClientB": "clientB@example.com",
    # Add more clients as needed
}

templates_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"])
)

if EMAIL_PROVIDER_NAME == "sendgrid":
    email_provider = SendGridProvider()
elif EMAIL_PROVIDER_NAME == "ses":
    email_provider = SESProvider()
else:
    raise RuntimeError(f"Unknown EMAIL_PROVIDER '{EMAIL_PROVIDER_NAME}'")

class ContactForm(BaseModel):
    client_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=1000)
    recaptcha_token: str

# async def verify_recaptcha(token: str) -> bool:
#     url = "https://www.google.com/recaptcha/api/siteverify"
#     data = {"secret": RECAPTCHA_SECRET, "response": token}
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, data=data)
#         result = response.json()
#         logging.info(f"reCAPTCHA response: {result}")
#         return result.get("success", False)  # For v2 Invisible


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}


# @app.post("/send-email")
# async def send_email(form: ContactForm):
#     try:
#         if not await verify_recaptcha(form.recaptcha_token):
#             raise HTTPException(status_code=400, detail="reCAPTCHA validation failed")

#         to_email = CLIENT_EMAIL_MAP.get(form.client_id)
#         if not to_email:
#             raise HTTPException(status_code=400, detail="Unknown client_id")

#         html_template = templates_env.get_template("email_template.html")
#         plain_template = templates_env.get_template("email_template.txt")

#         html_content = html_template.render(name=form.name, email=form.email, message=form.message)
#         plain_text = plain_template.render(name=form.name, email=form.email, message=form.message)

#         subject = f"New Contact Form Submission from {form.name}"

#         sent = email_provider.send_email(
#             subject=subject,
#             to_email=to_email,
#             from_email=FROM_EMAIL,
#             plain_text=plain_text,
#             html_content=html_content,
#             reply_to=form.email,
#         )

#         if not sent:
#             raise HTTPException(status_code=500, detail="Failed to send email")

#         return {"status": "success"}

#     except Exception as e:
#         logging.error(f"Exception in send_email: {e}")
#         logging.error(traceback.format_exc())
#         raise HTTPException(status_code=500, detail="Internal server error")