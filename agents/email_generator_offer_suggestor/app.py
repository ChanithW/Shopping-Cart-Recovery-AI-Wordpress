from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import EmailData, GeneratedEmail, Offer
from ..shared.gemini_client import generate_email_content, suggest_offers
from ..shared.utils import apply_business_rules
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = FastAPI(title="Email Generator & Offer Suggestor Agent")
security = HTTPBearer()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/generate-email", response_model=GeneratedEmail)
def generate_email(data: EmailData, token: str = Depends(verify_token)):
    # Use Gemini for personalized content
    content = generate_email_content(data)
    # Suggest offers based on rules + LLM
    offers = suggest_offers(data)
    # Apply business rules (e.g., loyal customer -> 10% coupon)
    final_offers = apply_business_rules(offers, data.persona)

    # Construct email
    subject = content.get("subject", "We Miss You! Complete Your Purchase")
    body = templates.get_template("email_template.html").render(
        subject=subject,
        name=data.name,
        items=data.items,
        recommendations=data.recommendations,
        offers=final_offers,
        body=content.get("body", ""),
        user_id=data.user_id,
        email=data.email
    )

    # Dispatch email securely
    send_email(data.email, subject, body)

    # Note: Database logging is now handled by WordPress plugin

    return GeneratedEmail(subject=subject, body=body, offers=final_offers)

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv("SMTP_FROM")
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.sendmail(msg['From'], to_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        # Don't raise exception - just log the error for now

@app.get("/track-open")
def track_open(user_id: str, email: str):
    # Note: Tracking is now handled by WordPress plugin
    return {"status": "tracked"}

@app.get("/track-click")
def track_click(user_id: str, email: str):
    # Note: Tracking is now handled by WordPress plugin
    return {"status": "tracked"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)