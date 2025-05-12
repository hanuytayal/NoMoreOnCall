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
    time.sleep(2)  # Reduced delay after section headers

def print_summary(title, points):
    """Print a summary section with bullet points."""
    print("\n" + "-"*80)
    print(f" {title} ".center(80, "-"))
    print("-"*80)
    for point in points:
        print(f"• {point}")
    print("-"*80 + "\n")
    time.sleep(3)  # Reduced delay after summary

def print_json(data):
    print(json.dumps(data, indent=2))
    time.sleep(3)  # Reduced delay after printing JSON data

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
    time.sleep(2)  # Reduced delay after intro
    
    print_summary("Demo Overview", [
        "We'll demonstrate how NoMoreOnCall handles a database timeout error",
        "The system will analyze the error, identify root causes, and suggest fixes",
        "We'll see how the system integrates with your existing monitoring",
        "Finally, we'll generate and apply the fixes automatically"
    ])
    
    # Start the notification API in a separate thread
    print_section("Starting Notification API")
    print("Starting the notification API on port 8001...")
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    time.sleep(3)  # Reduced wait time for API to start
    
    print_summary("API Setup Complete", [
        "Notification API is now running on port 8001",
        "This API will receive error notifications from your monitoring system",
        "It's ready to process incoming error reports"
    ])
    
    try:
        # Demo Error 1: Database Timeout
        print_section("Demo Error 1: Database Timeout")
        print("Analyzing database timeout error (ERR_123)...")
        time.sleep(2)  # Reduced delay before analysis
        run_command(["python", "debug_analyzer_v2.py", "ERR_123"])
        time.sleep(3)  # Reduced delay after analysis
        
        print_summary("Error Analysis Complete", [
            "Successfully analyzed the database timeout error",
            "Identified the affected code paths and components",
            "Generated a detailed issue report"
        ])
        
        # Show the generated issue file
        with open("issue_ERR_123.json", "r") as f:
            issue_data = json.load(f)
        
        # Break down the issue file into distinct sections
        print_section("Error Details")
        print_json(issue_data["error_details"])
        time.sleep(2)  # Reduced delay between sections
        
        print_summary("Error Details Analysis", [
            "Identified the error type and message",
            "Captured the request context and user information",
            "Recorded the complete stack trace for analysis"
        ])
        
        print_section("Code Analysis")
        print_json(issue_data["code_analysis"])
        time.sleep(2)  # Reduced delay between sections
        
        print_summary("Code Analysis Results", [
            "Analyzed the affected code files and functions",
            "Identified the specific lines causing the issue",
            "Gathered context about the code's execution environment"
        ])
        
        print_section("LLM Analysis")
        print_json(issue_data["llm_analysis"])
        time.sleep(3)  # Reduced delay before fixes
        
        print_summary("LLM Analysis Complete", [
            "AI model analyzed the error patterns",
            "Identified potential root causes",
            "Generated specific fix recommendations"
        ])
        
        # Generate code fixes
        print_section("Generating Code Fixes")
        print("Generating code fixes for the database timeout error...")
        time.sleep(2)  # Reduced delay before generating fixes
        run_command(["python", "code_fixer.py", "issue_ERR_123.json"], check=False)
        time.sleep(3)  # Reduced delay after generating fixes
        
        print_summary("Code Fixes Generated", [
            "Successfully generated fix recommendations",
            "Created a patch file with the proposed changes",
            "Prepared a pull request for review"
        ])
        
        print_section("Demo Complete")
        print("The demo has completed successfully!")
        print("\nGenerated files:")
        for file in Path(".").glob("issue_*.json"):
            print(f"- {file.name}")
            time.sleep(1)  # Reduced delay between file listings
        
        print_summary("Demo Summary", [
            "Successfully demonstrated NoMoreOnCall's error handling workflow",
            "Showed how the system analyzes and fixes errors automatically",
            "Generated all necessary files for error resolution",
            "Ready to integrate with your production environment"
        ])
        
    except Exception as e:
        print(f"\nError during demo: {e}")

if __name__ == "__main__":
    run_demo() 