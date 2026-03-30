#!/usr/bin/env python3
"""
Entry point for biz.rw backend.
Run from the project root:  python run.py
"""
import uvicorn
import os
import sys

# Add backend directory to sys.path so absolute imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=os.environ.get("RELOAD", "true").lower() == "true",
        log_level="info",
    )
