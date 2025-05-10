import subprocess
import time
import json
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

@app.post("/notify")
async def notify_error(error_data: dict):
    # Remove root_cause and suggested_fixes from the notification payload
    notification_data = {
        "error_id": error_data["error_id"],
        "timestamp": error_data["timestamp"],
        "type": error_data["error_details"]["type"],
        "message": error_data["error_details"]["message"],
        "request_id": error_data["error_details"]["request_id"],
        "user_id": error_data["error_details"]["user_id"],
        "endpoint": error_data["error_details"]["endpoint"],
        "stack_trace": error_data["error_details"]["stack_trace"]
    }
    print(f"Received notification: {json.dumps(notification_data, indent=2)}")
    return {"status": "Notification received"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8001)

def print_section(title):
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80 + "\n")

def print_json(data):
    print(json.dumps(data, indent=2))

def run_command(cmd, check=True):
    """Run a command and handle errors gracefully."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}:")
        print(f"Exit code: {e.returncode}")
        print(f"Output: {e.output}")
        if check:
            raise
        return None

def run_demo():
    print_section("NoMoreOnCall Demo")
    print("This demo will show how NoMoreOnCall analyzes and fixes errors.\n")
    
    # Start the notification API in a separate thread
    print_section("Starting Notification API")
    print("Starting the notification API on port 8001...")
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    time.sleep(2)  # Wait for API to start
    
    try:
        # Demo Error 1: Database Timeout
        print_section("Demo Error 1: Database Timeout")
        print("Analyzing database timeout error (ERR_123)...")
        run_command(["python", "debug_analyzer_v2.py", "ERR_123"])
        
        # Show the generated issue file
        with open("issue_ERR_123.json", "r") as f:
            issue_data = json.load(f)
        
        # Break down the issue file into distinct sections
        print_section("Error Details")
        print_json(issue_data["error_details"])
        
        print_section("Code Analysis")
        print_json(issue_data["code_analysis"])
        
        print_section("LLM Analysis")
        print_json(issue_data["llm_analysis"])
        
        # Generate code fixes
        print_section("Generating Code Fixes")
        print("Generating code fixes for the database timeout error...")
        run_command(["python", "code_fixer.py", "issue_ERR_123.json"], check=False)
        
        print_section("Demo Complete")
        print("The demo has completed successfully!")
        print("\nGenerated files:")
        for file in Path(".").glob("issue_*.json"):
            print(f"- {file.name}")
        
    except Exception as e:
        print(f"\nError during demo: {e}")

if __name__ == "__main__":
    run_demo() 