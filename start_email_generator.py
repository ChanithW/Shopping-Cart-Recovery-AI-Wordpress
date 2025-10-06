#!/usr/bin/env python3
"""
Simple startup script for the email generator service.
"""

import uvicorn
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    print("Starting Email Generator Service...")
    uvicorn.run(
        "agents.email_generator_offer_suggestor.app:app",
        host="0.0.0.0",
        port=8002,
        log_level="info",
        access_log=True
    )