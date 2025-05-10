import os
import json
import sys
from datetime import datetime

def analyze_error(error_id):
    # Simulate error analysis
    error_details = {
        "error_id": error_id,
        "type": "DatabaseError" if error_id == "ERR_123" else "AuthenticationError",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "Database connection timeout" if error_id == "ERR_123" else "Invalid authentication token",
        "request_id": "req_123" if error_id == "ERR_123" else "req_789",
        "user_id": "user_456" if error_id == "ERR_123" else "user_123",
        "endpoint": "/api/v1/users" if error_id == "ERR_123" else "/api/v1/auth",
        "stack_trace": [
            "app/database.py:45: connect()",
            "app/models.py:23: get_user()",
            "app/views.py:12: user_view()"
        ] if error_id == "ERR_123" else [
            "app/auth.py:67: validate_token()",
            "app/middleware.py:34: auth_middleware()",
            "app/views.py:45: protected_view()"
        ]
    }

    code_analysis = [
        {
            "file_path": "app/database.py",
            "error_lines": [45],
            "context_lines": {
                "43": "def connect():",
                "44": "    try:",
                "45": "        db = Database(timeout=5)  # Error line",
                "46": "        return db.connect()",
                "47": "    except Exception as e:"
            },
            "blame_info": {
                "45": {
                    "author": "John Doe",
                    "commit": "abc123",
                    "date": "2024-02-19"
                }
            }
        },
        {
            "file_path": "app/models.py",
            "error_lines": [23],
            "context_lines": {
                "21": "def get_user(user_id):",
                "22": "    try:",
                "23": "        return db.query(f'SELECT * FROM users WHERE id = {user_id}')",
                "24": "    except Exception as e:",
                "25": "        raise DatabaseError(str(e))"
            },
            "blame_info": {
                "23": {
                    "author": "Jane Smith",
                    "commit": "def456",
                    "date": "2024-02-18"
                }
            }
        }
    ] if error_id == "ERR_123" else [
        {
            "file_path": "app/auth.py",
            "error_lines": [67],
            "context_lines": {
                "65": "def validate_token(token):",
                "66": "    try:",
                "67": "        if not token or len(token) < 32:  # Error line",
                "68": "            raise AuthenticationError('Invalid token')",
                "69": "        return decode_token(token)"
            },
            "blame_info": {
                "67": {
                    "author": "Bob Wilson",
                    "commit": "ghi789",
                    "date": "2024-02-17"
                }
            }
        },
        {
            "file_path": "app/middleware.py",
            "error_lines": [34],
            "context_lines": {
                "32": "def auth_middleware(request):",
                "33": "    try:",
                "34": "        token = request.headers.get('Authorization')",
                "35": "        if not token:",
                "36": "            raise AuthenticationError('No token provided')"
            },
            "blame_info": {
                "34": {
                    "author": "Alice Brown",
                    "commit": "jkl012",
                    "date": "2024-02-16"
                }
            }
        }
    ]

    llm_analysis = {
        "root_cause": "Insufficient timeout value for database connection" if error_id == "ERR_123" else "Insufficient token validation",
        "code_level_explanation": "The database connection is timing out because the timeout value of 5 seconds is too low for the current load. The error occurs in database.py when trying to establish a connection." if error_id == "ERR_123" else "The authentication token validation is failing because the token length check is too strict. The error occurs in auth.py when validating the token.",
        "suggested_fixes": [
            "Increase database connection timeout to 30 seconds",
            "Implement connection pooling",
            "Add retry mechanism with exponential backoff"
        ] if error_id == "ERR_123" else [
            "Update token validation logic to handle different token formats",
            "Add better error messages for token validation failures",
            "Implement token refresh mechanism"
        ],
        "prevention_measures": [
            "Implement circuit breakers for database operations",
            "Add monitoring for database connection metrics",
            "Set up alerts for connection timeouts"
        ] if error_id == "ERR_123" else [
            "Add comprehensive token validation tests",
            "Implement token blacklisting for revoked tokens",
            "Set up monitoring for authentication failures"
        ]
    }

    git_commits = [
        {
            "hash": "abc123",
            "author": "John Doe",
            "date": "2024-02-19",
            "message": "Update app/database.py",
            "files_changed": ["app/database.py"]
        },
        {
            "hash": "def456",
            "author": "Jane Smith",
            "date": "2024-02-18",
            "message": "Update app/models.py",
            "files_changed": ["app/models.py"]
        }
    ] if error_id == "ERR_123" else [
        {
            "hash": "ghi789",
            "author": "Bob Wilson",
            "date": "2024-02-17",
            "message": "Update app/auth.py",
            "files_changed": ["app/auth.py"]
        },
        {
            "hash": "jkl012",
            "author": "Alice Brown",
            "date": "2024-02-16",
            "message": "Update app/middleware.py",
            "files_changed": ["app/middleware.py"]
        }
    ]

    issue_data = {
        "error_id": error_id,
        "timestamp": datetime.now().isoformat(),
        "error_details": error_details,
        "code_analysis": code_analysis,
        "llm_analysis": llm_analysis,
        "git_commits": git_commits
    }

    # Save to file
    filename = f"issue_{error_id}.json"
    with open(filename, "w") as f:
        json.dump(issue_data, f, indent=2)
    print(f"Generated Issue File:\n{json.dumps(issue_data, indent=2)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python debug_analyzer_v2.py <error_id>")
        sys.exit(1)
    analyze_error(sys.argv[1]) 