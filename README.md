# NoMoreOnCall

A comprehensive error analysis and debugging system that helps developers quickly identify and fix application errors.

## Features
- Analyzes errors and generates detailed reports
- Provides code-level context and blame information
- Suggests fixes and prevention measures
- Generates code change suggestions for a wide range of error types

## Components

### 1. Debug Analyzer
- Fetches error details from an API (or uses mock data for testing)
- Analyzes related code files with context and blame information
- Provides root cause analysis and suggested fixes
- Generates structured JSON reports

### 2. Notification API (Integrated)
- Receives notifications about analyzed errors (now integrated into the demo script)
- Logs notification details
- Returns acknowledgment responses

### 3. Code Fixer
- Reads error analysis from JSON files
- Suggests specific code changes for a variety of error types
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
4. **Create a `.env` file** (if needed for custom API keys):
   ```env
   DEBUG_API_BASE_URL=http://localhost:8000
   DEBUG_API_KEY=dummy_key
   REPO_PATH=.
   ```

## Quick Demo
Run the demo script to see the system in action:
```sh
python demo.py
```

The demo will:
1. Start the notification API (in-process)
2. Analyze two example errors:
   - Database timeout error (ERR_123)
   - Authentication error (ERR_456)
3. Generate code fixes for both errors
4. Show the results in a clear format

## Supported Error Types & Fixes
The code fixer currently supports automatic suggestions for:
- **DatabaseError**: Increase timeouts, parameterize queries, add pooling
- **AuthenticationError**: Improve token validation, better header extraction
- **ConnectionError**: Add retry logic
- **TimeoutError**: Increase/double timeouts
- **ValidationError**: Add comprehensive input validation
- **ResourceNotFoundError**: Add default values to lookups
- **PermissionError**: Add role-based permission checks
- **RateLimitError**: Add rate limiting decorators
- **MemoryError**: Use generators, memory-efficient data structures
- **ConcurrencyError**: Add thread safety, locks
- **ConfigurationError**: Add default values, validate env vars
- **SecurityError**: Add password hashing, secure token handling
- **NetworkError**: Add timeouts/retries, connection error handling
- **FileSystemError**: Use context managers, check file existence
- **SerializationError**: Safe JSON/pickle serialization
- **Generic errors**: Add better error handling and logging

## Manual Usage

### 1. Run the Debug Analyzer
```sh
python debug_analyzer_v2.py ERR_123
```

### 2. Generate Code Fixes
```sh
python code_fixer.py issue_ERR_123.json
```

## Testing
The system includes mock data for testing:
- `ERR_123`: Database connection timeout error
- `ERR_456`: Authentication token validation error
- `ERR_789`: Memory error (large list allocation)

You can add your own issue files to test other error types.

## Documentation
- [Architecture](ARCHITECTURE.md): Technical architecture and component design

## License
MIT
