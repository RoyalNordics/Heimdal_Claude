# Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import httpx
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Heimdal Webhook")

class WebhookRequest(BaseModel):
    prompt: str
    type: str = "code"  # code, execution, or prompt
    language: Optional[str] = "python"
    component: Optional[str] = None  # backend, frontend, database, etc.

@app.get("/")
async def root():
    return {"status": "Heimdal webhook is running"}

@app.post("/webhook")
async def webhook(request: WebhookRequest):
    try:
        # Log the incoming request
        print(f"Received webhook request: {request.dict()}")
        
        if request.type == "code":
            # This will be enhanced to process code from Claude
            return {
                "status": "success", 
                "message": f"Received {request.language} code for {request.component}",
                "data": {
                    "received": request.prompt
                }
            }
        elif request.type == "execution":
            # This will be enhanced to execute code
            return {
                "status": "success",
                "message": "Execution request received",
                "data": {
                    "result": "Code execution simulation (to be implemented)"
                }
            }
        else:
            # This will be enhanced to process prompts for LangChain
            return {
                "status": "success",
                "message": "Prompt received",
                "data": {
                    "result": "Prompt processing simulation (to be implemented)"
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

echo "Created main.py"
