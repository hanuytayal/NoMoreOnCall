import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@dataclass
class ErrorDetails:
    error_id: str
    type: str
    timestamp: str
    message: str
    request_id: str
    user_id: str
    endpoint: str
    stack_trace: List[str]

@dataclass
class CodeAnalysis:
    file_path: str
    error_lines: List[int]
    context_lines: Dict[int, str]
    blame_info: Dict[int, Dict[str, str]]

@dataclass
class LLMAnalysis:
    root_cause: str
    code_level_explanation: str
    suggested_fixes: List[str]
    prevention_measures: List[str]

@dataclass
class GitCommit:
    hash: str
    author: str
    date: str
    message: str
    files_changed: List[str]

class DebugAnalyzer:
    def __init__(self):
        self.api_base_url = os.getenv('DEBUG_API_BASE_URL', 'http://localhost:8000')
        self.api_key = os.getenv('DEBUG_API_KEY', 'dummy_key')
        self.repo_path = os.getenv('REPO_PATH', '.')
        
    def _fetch_error_details(self, error_id: str) -> ErrorDetails:
        """Fetch error details from API"""
        # For testing, return mock data
        if error_id == "ERR_123":
            return ErrorDetails(
                error_id="ERR_123",
                type="DatabaseError",
                timestamp="2024-02-20T10:30:00Z",
                message="Database connection timeout",
                request_id="req_123",
                user_id="user_456",
                endpoint="/api/v1/users",
                stack_trace=[
                    "app/database.py:45: connect()",
                    "app/models.py:23: get_user()",
                    "app/views.py:12: user_view()"
                ]
            )
        elif error_id == "ERR_456":
            return ErrorDetails(
                error_id="ERR_456",
                type="AuthenticationError",
                timestamp="2024-02-20T11:15:00Z",
                message="Invalid authentication token",
                request_id="req_789",
                user_id="user_123",
                endpoint="/api/v1/auth",
                stack_trace=[
                    "app/auth.py:67: validate_token()",
                    "app/middleware.py:34: auth_middleware()",
                    "app/views.py:45: protected_view()"
                ]
            )
        else:
            raise ValueError(f"Unknown error ID: {error_id}")

    def _analyze_code(self, error_details: ErrorDetails) -> List[CodeAnalysis]:
        """Analyze code related to the error"""
        # For testing, return mock data
        if error_details.error_id == "ERR_123":
            return [
                CodeAnalysis(
                    file_path="app/database.py",
                    error_lines=[45],
                    context_lines={
                        43: "def connect():",
                        44: "    try:",
                        45: "        db = Database(timeout=5)  # Error line",
                        46: "        return db.connect()",
                        47: "    except Exception as e:"
                    },
                    blame_info={
                        45: {
                            "author": "John Doe",
                            "commit": "abc123",
                            "date": "2024-02-19"
                        }
                    }
                ),
                CodeAnalysis(
                    file_path="app/models.py",
                    error_lines=[23],
                    context_lines={
                        21: "def get_user(user_id):",
                        22: "    try:",
                        23: "        return db.query(f'SELECT * FROM users WHERE id = {user_id}')",
                        24: "    except Exception as e:",
                        25: "        raise DatabaseError(str(e))"
                    },
                    blame_info={
                        23: {
                            "author": "Jane Smith",
                            "commit": "def456",
                            "date": "2024-02-18"
                        }
                    }
                )
            ]
        else:  # ERR_456
            return [
                CodeAnalysis(
                    file_path="app/auth.py",
                    error_lines=[67],
                    context_lines={
                        65: "def validate_token(token):",
                        66: "    try:",
                        67: "        if not token or len(token) < 32:  # Error line",
                        68: "            raise AuthenticationError('Invalid token')",
                        69: "        return decode_token(token)"
                    },
                    blame_info={
                        67: {
                            "author": "Bob Wilson",
                            "commit": "ghi789",
                            "date": "2024-02-17"
                        }
                    }
                ),
                CodeAnalysis(
                    file_path="app/middleware.py",
                    error_lines=[34],
                    context_lines={
                        32: "def auth_middleware(request):",
                        33: "    try:",
                        34: "        token = request.headers.get('Authorization')",
                        35: "        if not token:",
                        36: "            raise AuthenticationError('No token provided')"
                    },
                    blame_info={
                        34: {
                            "author": "Alice Brown",
                            "commit": "jkl012",
                            "date": "2024-02-16"
                        }
                    }
                )
            ]

    def _analyze_with_llm(self, error_details: ErrorDetails, code_analysis: List[CodeAnalysis]) -> LLMAnalysis:
        """Analyze error with language model"""
        # For testing, return mock data
        if error_details.error_id == "ERR_123":
            return LLMAnalysis(
                root_cause="Insufficient timeout value for database connection",
                code_level_explanation="The database connection is timing out because the timeout value of 5 seconds is too low for the current load. The error occurs in database.py when trying to establish a connection.",
                suggested_fixes=[
                    "Increase database connection timeout to 30 seconds",
                    "Implement connection pooling",
                    "Add retry mechanism with exponential backoff"
                ],
                prevention_measures=[
                    "Implement circuit breakers for database operations",
                    "Add monitoring for database connection metrics",
                    "Set up alerts for connection timeouts"
                ]
            )
        else:  # ERR_456
            return LLMAnalysis(
                root_cause="Insufficient token validation",
                code_level_explanation="The authentication token validation is failing because the token length check is too strict. The error occurs in auth.py when validating the token.",
                suggested_fixes=[
                    "Update token validation logic to handle different token formats",
                    "Add better error messages for token validation failures",
                    "Implement token refresh mechanism"
                ],
                prevention_measures=[
                    "Add comprehensive token validation tests",
                    "Implement token blacklisting for revoked tokens",
                    "Set up monitoring for authentication failures"
                ]
            )

    def _get_git_commits(self, code_analysis: List[CodeAnalysis]) -> List[GitCommit]:
        """Get git commits related to the error"""
        # For testing, return mock data
        commits = []
        for analysis in code_analysis:
            for line, blame in analysis.blame_info.items():
                commits.append(GitCommit(
                    hash=blame["commit"],
                    author=blame["author"],
                    date=blame["date"],
                    message=f"Update {analysis.file_path}",
                    files_changed=[analysis.file_path]
                ))
        return commits

    def _create_issue_file(self, error_id: str, error_details: ErrorDetails,
                          code_analysis: List[CodeAnalysis], llm_analysis: LLMAnalysis,
                          git_commits: List[GitCommit]) -> str:
        """Create issue file content"""
        issue_data = {
            "error_id": error_id,
            "timestamp": datetime.now().isoformat(),
            "error_details": asdict(error_details),
            "code_analysis": [asdict(analysis) for analysis in code_analysis],
            "llm_analysis": asdict(llm_analysis),
            "git_commits": [asdict(commit) for commit in git_commits]
        }
        return json.dumps(issue_data, indent=2)

    def analyze_error(self, error_id: str) -> Dict:
        """Analyze an error and generate a detailed report"""
        try:
            # Fetch error details from API
            error_details = self._fetch_error_details(error_id)
            
            # Analyze related code
            code_analysis = self._analyze_code(error_details)
            
            # Get LLM analysis
            llm_analysis = self._analyze_with_llm(error_details, code_analysis)
            
            # Get git commits
            git_commits = self._get_git_commits(code_analysis)
            
            # Create issue file
            issue_content = self._create_issue_file(
                error_id,
                error_details,
                code_analysis,
                llm_analysis,
                git_commits
            )
            
            # Save issue file
            issue_file = f"issue_{error_id}.json"
            with open(issue_file, 'w') as f:
                f.write(issue_content)
            
            logger.info(f"Issue file created: {issue_file}")

            # Notify API
            try:
                notify_payload = {
                    'error_id': error_id,
                    'status': 'analyzed',
                    'issue_file': issue_file,
                    'summary': {
                        'type': error_details.type,
                        'message': error_details.message,
                        'root_cause': llm_analysis.root_cause,
                        'suggested_fixes': llm_analysis.suggested_fixes
                    }
                }
                resp = requests.post('http://localhost:8001/notify', json=notify_payload, timeout=5)
                logger.info(f"Notification sent: {resp.status_code} {resp.text}")
            except Exception as notify_err:
                logger.error(f"Failed to notify API: {notify_err}")
            
            return {
                'error_details': error_details,
                'code_analysis': code_analysis,
                'llm_analysis': llm_analysis,
                'git_commits': git_commits
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {error_id}: {str(e)}")
            raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python debug_analyzer_v2.py <error_id>")
        sys.exit(1)
        
    error_id = sys.argv[1]
    analyzer = DebugAnalyzer()
    result = analyzer.analyze_error(error_id)
    
    # Print summary
    print("\nAnalysis Summary:")
    print(f"Error ID: {result['error_details'].error_id}")
    print(f"Type: {result['error_details'].type}")
    print(f"Message: {result['error_details'].message}")
    print(f"\nRoot Cause: {result['llm_analysis'].root_cause}")
    print("\nSuggested Fixes:")
    for fix in result['llm_analysis'].suggested_fixes:
        print(f"- {fix}")
    print("\nGit Commits Involved:")
    for commit in result['git_commits']:
        print(f"- {commit.hash} by {commit.author}") 