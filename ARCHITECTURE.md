# NoMoreOnCall Architecture

## Overview
NoMoreOnCall is a comprehensive error analysis and debugging system that helps developers quickly identify and fix application errors. The system consists of three main components:

1. **Debug Analyzer**: Analyzes errors and generates detailed reports
2. **Notification API**: Receives and processes analysis notifications
3. **Code Fixer**: Suggests code changes based on error analysis

## System Components

### 1. Debug Analyzer (`debug_analyzer_v2.py`)
The core component that analyzes errors and generates detailed reports.

#### Key Classes
- `ErrorDetails`: Stores error information
  - `error_id`: Unique identifier for the error
  - `type`: Error type (e.g., DatabaseError, AuthenticationError)
  - `message`: Error message
  - `stack_trace`: List of stack trace lines
  - Additional metadata (timestamp, request_id, etc.)

- `CodeAnalysis`: Contains code analysis results
  - `file_path`: Path to the analyzed file
  - `error_lines`: List of line numbers with errors
  - `context_lines`: Dictionary of line numbers to code content
  - `blame_info`: Git blame information for error lines

- `LLMAnalysis`: Stores analysis results
  - `root_cause`: Identified root cause of the error
  - `code_level_explanation`: Detailed explanation
  - `suggested_fixes`: List of suggested fixes
  - `prevention_measures`: List of prevention measures

- `GitCommit`: Tracks git commit information
  - `hash`: Commit hash
  - `author`: Commit author
  - `date`: Commit date
  - `message`: Commit message
  - `files_changed`: List of changed files

#### Main Methods
- `analyze_error(error_id)`: Main entry point
- `_fetch_error_details(error_id)`: Gets error details
- `_analyze_code(error_details)`: Analyzes related code
- `_analyze_with_llm(error_details, code_analysis)`: Gets LLM analysis
- `_get_git_commits(code_analysis)`: Gets git commit info
- `_create_issue_file(...)`: Generates JSON report

### 2. Notification API (`notification_api.py`)
A FastAPI-based service that receives and processes analysis notifications.

#### Endpoints
- `POST /notify`: Receives analysis notifications
  - Input: Error ID, status, issue file, summary
  - Output: Acknowledgment response

#### Features
- Asynchronous request handling
- JSON request/response format
- Logging of notifications

### 3. Code Fixer (`code_fixer.py`)
Suggests code changes based on error analysis.

#### Features
- Reads JSON analysis files
- Suggests specific code changes
- Generates PR descriptions
- Provides detailed explanations

## Data Flow
```
[Error Occurs]
     ↓
[Debug Analyzer]
     ↓
[Error Details] → [Code Analysis] → [LLM Analysis]
     ↓
[Issue File (JSON)]
     ↓
[Notification API]
     ↓
[Code Fixer]
     ↓
[Suggested Fixes]
```

## File Structure
```
/NoMoreOnCall
├── debug_analyzer_v2.py    # Main analyzer component
├── notification_api.py     # Notification service
├── code_fixer.py          # Code fix suggestions
├── requirements.txt       # Python dependencies
├── README.md             # Project overview
├── ARCHITECTURE.md       # This file
└── SYSTEM.md             # System documentation
```

## Environment Variables
- `DEBUG_API_BASE_URL`: Base URL for the debug API
- `DEBUG_API_KEY`: API key for authentication
- `REPO_PATH`: Path to the code repository

## Dependencies
- FastAPI: Web framework for the notification API
- Python-dotenv: Environment variable management
- Requests: HTTP client for API calls
- Uvicorn: ASGI server for the notification API

## Future Enhancements
1. Real API integration for error details
2. Actual code analysis using git blame
3. LLM integration for intelligent analysis
4. Web interface for viewing analysis results
5. Integration with issue tracking systems 