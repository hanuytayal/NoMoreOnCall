# NoMoreOnCall System

## Overview
NoMoreOnCall is a comprehensive error analysis and debugging system that helps developers quickly identify and fix application errors. The system consists of three main components:

1. **Debug Analyzer**: Analyzes errors and generates detailed reports
2. **Notification API**: Receives and processes analysis notifications
3. **Code Fixer**: Suggests code changes based on error analysis

## Components

### 1. Debug Analyzer (`debug_analyzer_v2.py`)
The core component that analyzes errors and generates detailed reports. Features:
- Fetches error details from an API (or uses mock data for testing)
- Analyzes related code files with context and blame information
- Provides root cause analysis and suggested fixes
- Generates structured JSON reports
- Sends notifications to the notification API

Key classes:
- `ErrorDetails`: Stores error information (ID, type, message, stack trace)
- `CodeAnalysis`: Contains code analysis results (file paths, error lines, context)
- `LLMAnalysis`: Stores analysis results (root cause, fixes, prevention measures)
- `GitCommit`: Tracks git commit information
- `DebugAnalyzer`: Main class that orchestrates the analysis process

### 2. Notification API (`notification_api.py`)
A FastAPI-based service that receives and processes analysis notifications. Features:
- Receives notifications about analyzed errors
- Logs notification details
- Returns acknowledgment responses

### 3. Code Fixer (`code_fixer.py`)
Suggests code changes based on error analysis. Features:
- Reads error analysis from JSON files
- Suggests specific code changes
- Generates PR descriptions
- Provides detailed explanations for suggested changes

## Data Flow
1. Error occurs in the application
2. Debug Analyzer receives error ID
3. Analyzer fetches error details and analyzes code
4. Analysis results are saved as JSON
5. Notification is sent to Notification API
6. Code Fixer reads analysis and suggests fixes

## File Structure
```
/NoMoreOnCall
├── debug_analyzer_v2.py    # Main analyzer component
├── notification_api.py     # Notification service
├── code_fixer.py          # Code fix suggestions
├── requirements.txt       # Python dependencies
├── README.md             # Project overview
├── ARCHITECTURE.md       # System architecture
└── SYSTEM.md             # This file
```

## Setup and Usage

### Prerequisites
- Python 3.9+
- Virtual environment (recommended)

### Installation
1. Create and activate virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```env
   DEBUG_API_BASE_URL=http://localhost:8000
   DEBUG_API_KEY=dummy_key
   REPO_PATH=.
   ```

### Running the System
1. Start the notification API:
   ```sh
   uvicorn notification_api:app --host 0.0.0.0 --port 8001 --reload
   ```

2. Run the debug analyzer:
   ```sh
   python debug_analyzer_v2.py ERR_123
   ```

3. Generate code fixes:
   ```sh
   python code_fixer.py issue_ERR_123.json
   ```

## Testing
The system includes mock data for testing:
- `ERR_123`: Database connection timeout error
- `ERR_456`: Authentication token validation error

## Future Enhancements
1. Real API integration for error details
2. Actual code analysis using git blame
3. LLM integration for intelligent analysis
4. Web interface for viewing analysis results
5. Integration with issue tracking systems 