# NoMoreOnCall

A comprehensive error analysis and debugging system that helps developers quickly identify and fix application errors.

## Features
- Analyzes errors and generates detailed reports
- Provides code-level context and blame information
- Suggests fixes and prevention measures
- Sends notifications about analyzed errors
- Generates code change suggestions

## Components

### 1. Debug Analyzer
- Fetches error details from an API (or uses mock data for testing)
- Analyzes related code files with context and blame information
- Provides root cause analysis and suggested fixes
- Generates structured JSON reports
- Sends notifications to the notification API

### 2. Notification API
- Receives notifications about analyzed errors
- Logs notification details
- Returns acknowledgment responses

### 3. Code Fixer
- Reads error analysis from JSON files
- Suggests specific code changes
- Generates PR descriptions
- Provides detailed explanations for suggested changes

## Setup
1. **Clone the repository**
2. **Create a virtual environment**:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Create a `.env` file**:
   ```env
   DEBUG_API_BASE_URL=http://localhost:8000
   DEBUG_API_KEY=dummy_key
   REPO_PATH=.
   ```

## Usage

### 1. Start the Notification API
```sh
uvicorn notification_api:app --host 0.0.0.0 --port 8001 --reload
```

### 2. Run the Debug Analyzer
```sh
python debug_analyzer_v2.py ERR_123
```

### 3. Generate Code Fixes
```sh
python code_fixer.py issue_ERR_123.json
```

## Testing
The system includes mock data for testing:
- `ERR_123`: Database connection timeout error
- `ERR_456`: Authentication token validation error

## Documentation
- [System Overview](SYSTEM.md): Detailed system architecture and functionality
- [Architecture](ARCHITECTURE.md): Technical architecture and component design

## License
MIT
