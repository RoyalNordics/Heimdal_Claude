import os
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI(title="Heimdal Webhook")

class WebhookRequest(BaseModel):
    prompt: str
    type: str = "code"
    language: Optional[str] = "python"
    component: Optional[str] = None
    
async def process_request(request_data: WebhookRequest):
    """Process the webhook request and create files based on the prompt."""
    try:
        # Extract file paths from the prompt
        lines = request_data.prompt.strip().split("\n")
        file_paths = []
        
        for line in lines:
            if " - " in line and any(line.strip().startswith(str(i) + ".") for i in range(1, 20)):
                # This line likely contains a file path
                parts = line.split(" - ", 1)
                if len(parts) == 2:
                    # Remove the number prefix
                    file_path = parts[0].split(".", 1)[1].strip()
                    file_paths.append(file_path)
        
        print(f"Extracted file paths: {file_paths}")
        
        # For now, just create empty files at these paths
        for file_path in file_paths:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Create an empty file
            with open(file_path, 'w') as f:
                f.write(f"// TODO: Implement {file_path}\n")
            
            print(f"Created file: {file_path}")
            
        return {"status": "success", "message": f"Created {len(file_paths)} files", "files": file_paths}
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {"status": "Heimdal webhook is running"}

@app.post("/webhook")
async def webhook(request: WebhookRequest, background_tasks: BackgroundTasks):
    print(f"Received webhook request: {request}")
    
    # Process the request in the background
    background_tasks.add_task(process_request, request)
    
    return {
        "status": "success", 
        "message": f"Received {request.language} code for {request.component}", 
        "data": {"received": request.prompt}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
