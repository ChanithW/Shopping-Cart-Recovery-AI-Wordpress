from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from .models import CartData, AbandonmentResponse
from ..shared.recommendation_engine import ProductRecommendationEngine
import os

app = FastAPI(title="Abandonment Detector Agent")
security = HTTPBearer()

# Simple auth check (replace with proper JWT) - made optional for WordPress integration
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials and credentials.credentials != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/detect-abandonment", response_model=AbandonmentResponse)
def detect_abandonment(data: CartData):
    # Check if abandoned: e.g., idle time > 1 minute and no checkout
    idle_threshold = 60  # 1 minute (60 seconds)
    if data.behavior.idle_time > idle_threshold:
        # Fetch product details and recommendations using TF-IDF engine
        try:
            rec_engine = ProductRecommendationEngine()
            recommendations = rec_engine.get_recommendations_for_cart([
                {
                    'name': item.name, 
                    'description': item.description, 
                    'category': item.category
                } for item in data.items
            ])
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            recommendations = [{"name": "Similar Product", "price": 50.0}]
        
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

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "abandonment-detector", "port": 8005}

@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Shopping Cart Recovery - Abandonment Detector Agent", "status": "running", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)