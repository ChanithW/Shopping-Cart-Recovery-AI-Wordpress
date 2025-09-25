from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from .models import CartData, AbandonmentResponse
from ..shared.gemini_client import get_product_recommendations  # Import from shared
import os

app = FastAPI(title="Abandonment Detector Agent")
security = HTTPBearer()

# Simple auth check (replace with proper JWT)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/detect-abandonment", response_model=AbandonmentResponse)
def detect_abandonment(data: CartData, token: str = Depends(verify_token)):
    # Check if abandoned: e.g., idle time > 10 minutes and no checkout
    idle_threshold = 60  # 1 minute
    if data.behavior.idle_time > idle_threshold:
        # Fetch product details and recommendations using IR (via Gemini or DB)
        recommendations = get_product_recommendations(data.items)
        
        # Note: Database logging is now handled by WordPress plugin
        
        return AbandonmentResponse(abandoned=True, data={
            "user_id": data.user_id,
            "email": data.email,
            "items": [item.model_dump() for item in data.items],
            "timestamp": data.timestamp,
            "behavior": data.behavior.model_dump(),
            "recommendations": recommendations
        })
    return AbandonmentResponse(abandoned=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)