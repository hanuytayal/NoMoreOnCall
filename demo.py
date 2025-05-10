import subprocess
import time
import json
import os
from pathlib import Path

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
    
    # Start the notification API
    print_section("Starting Notification API")
    print("Starting the notification API on port 8001...")
    api_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "notification_api:app", "--host", "0.0.0.0", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)  # Wait for API to start
    
    try:
        # Demo Error 1: Database Timeout
        print_section("Demo Error 1: Database Timeout")
        print("Analyzing database timeout error (ERR_123)...")
        run_command(["python", "debug_analyzer_v2.py", "ERR_123"])
        
        # Show the generated issue file
        print("\nGenerated Issue File:")
        with open("issue_ERR_123.json", "r") as f:
            issue_data = json.load(f)
            print_json(issue_data)
        
        # Demo Error 2: Authentication Error
        print_section("Demo Error 2: Authentication Error")
        print("Analyzing authentication error (ERR_456)...")
        run_command(["python", "debug_analyzer_v2.py", "ERR_456"])
        
        # Show the generated issue file
        print("\nGenerated Issue File:")
        with open("issue_ERR_456.json", "r") as f:
            issue_data = json.load(f)
            print_json(issue_data)
        
        # Generate code fixes
        print_section("Generating Code Fixes")
        print("Generating code fixes for both errors...")
        run_command(["python", "code_fixer.py", "issue_ERR_123.json"], check=False)
        run_command(["python", "code_fixer.py", "issue_ERR_456.json"], check=False)
        
        print_section("Demo Complete")
        print("The demo has completed successfully!")
        print("\nGenerated files:")
        for file in Path(".").glob("issue_*.json"):
            print(f"- {file.name}")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
    finally:
        # Cleanup
        print_section("Cleaning Up")
        print("Stopping the notification API...")
        api_process.terminate()
        api_process.wait()

if __name__ == "__main__":
    run_demo() 