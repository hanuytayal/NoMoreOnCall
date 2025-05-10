import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any
import re
import itertools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class CodeChange:
    file_path: str
    original_code: str
    new_code: str
    line_number: int
    description: str
    author: str
    commit_hash: str

class CodeFixer:
    def __init__(self, issue_file: str):
        self.issue_file = issue_file
        self.issue_data = self._load_issue_file()
    
    def _load_issue_file(self) -> Dict[str, Any]:
        """Load and parse the issue file."""
        try:
            with open(self.issue_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading issue file: {e}")
            raise
    
    def suggest_code_changes(self) -> List[CodeChange]:
        """Generate code change suggestions based on the issue analysis."""
        changes = []
        
        # Process each file in the code analysis
        for file_analysis in self.issue_data.get('code_analysis', []):
            file_path = file_analysis['file_path']
            
            # Process each error line
            for line_number in file_analysis['error_lines']:
                context = file_analysis['context_lines']
                blame = file_analysis['blame_info'].get(str(line_number), {})
                
                # Get the original code
                original_code = context.get(str(line_number), '')
                
                # Generate new code based on the error type
                error_type = self.issue_data['error_details']['type']
                new_code = self._generate_fix(error_type, original_code, context)
                
                # Create code change suggestion
                change = CodeChange(
                    file_path=file_path,
                    original_code=original_code,
                    new_code=new_code,
                    line_number=line_number,
                    description=self.issue_data['llm_analysis']['suggested_fixes'][0],
                    author=blame.get('author', 'Unknown'),
                    commit_hash=blame.get('commit', 'Unknown')
                )
                changes.append(change)
        
        return changes
    
    def _generate_fix(self, error_type: str, code: str, context: Dict[str, str]) -> str:
        """Generate appropriate fix based on error type."""
        fix_methods = {
            'DatabaseError': self._fix_database_error,
            'AuthenticationError': self._fix_auth_error,
            'ConnectionError': self._fix_connection_error,
            'TimeoutError': self._fix_timeout_error,
            'ValidationError': self._fix_validation_error,
            'ResourceNotFoundError': self._fix_resource_not_found,
            'PermissionError': self._fix_permission_error,
            'RateLimitError': self._fix_rate_limit_error,
            'MemoryError': self._fix_memory_error,
            'ConcurrencyError': self._fix_concurrency_error,
            'ConfigurationError': self._fix_configuration_error,
            'SecurityError': self._fix_security_error,
            'NetworkError': self._fix_network_error,
            'FileSystemError': self._fix_filesystem_error,
            'SerializationError': self._fix_serialization_error
        }
        
        fix_method = fix_methods.get(error_type, self._fix_generic_error)
        return fix_method(code, context)
    
    def _fix_database_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for database errors."""
        if 'timeout=5' in code:
            return code.replace('timeout=5', 'timeout=30')
        elif 'db.query(' in code:
            # Add parameterized query
            return re.sub(r'db\.query\((.*?)\)', r'db.query("SELECT * FROM users WHERE id = ?", [\1])', code)
        elif 'connect()' in code:
            # Add connection pooling
            return code.replace('connect()', 'connect(pool_size=5, max_overflow=10)')
        return code
    
    def _fix_auth_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for authentication errors."""
        if 'len(token) < 32' in code:
            return code.replace('len(token) < 32', 'not is_valid_token_format(token)')
        elif 'Authorization' in code:
            # Add better token extraction
            return code.replace(
                "token = request.headers.get('Authorization')",
                "token = request.headers.get('Authorization', '').replace('Bearer ', '')"
            )
        return code
    
    def _fix_connection_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for connection errors."""
        if 'connect()' in code:
            # Add retry mechanism
            return f"""@retry(max_attempts=3, delay=1)
{code}"""
        return code
    
    def _fix_timeout_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for timeout errors."""
        if 'timeout=' in code:
            # Double the timeout value
            return re.sub(r'timeout=(\d+)', lambda m: f'timeout={int(m.group(1)) * 2}', code)
        return code
    
    def _fix_validation_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for validation errors."""
        if 'if not' in code:
            # Add more comprehensive validation
            return code.replace('if not', 'if not is_valid_input(')
        return code
    
    def _fix_resource_not_found(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for resource not found errors."""
        if 'get(' in code:
            # Add default value
            return re.sub(r'\.get\((.*?)\)', r'.get(\1, None)', code)
        return code
    
    def _fix_permission_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for permission errors."""
        if 'check_permission' in code:
            # Add role-based check
            return code.replace('check_permission', 'check_permission_with_roles')
        return code
    
    def _fix_rate_limit_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for rate limit errors."""
        if 'request' in code:
            # Add rate limiting
            return f"""@rate_limit(max_requests=100, window=60)
{code}"""
        return code

    def _fix_memory_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for memory errors."""
        if 'list(' in code:
            # Convert list to generator
            return code.replace('list(', 'generator(')
        elif 'dict(' in code:
            # Use defaultdict for memory efficiency
            return code.replace('dict(', 'defaultdict(')
        elif 'for' in code and 'in' in code:
            # Add memory-efficient iteration
            return code.replace('for', 'for _ in itertools.islice(')
        return code

    def _fix_concurrency_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for concurrency errors."""
        if 'global' in code:
            # Add thread-safe access
            return f"""@thread_safe
{code}"""
        elif 'shared_resource' in code:
            # Add lock mechanism
            return f"""with lock:
    {code}"""
        return code

    def _fix_configuration_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for configuration errors."""
        if 'config.get(' in code:
            # Add default values and validation
            return re.sub(r'config\.get\((.*?)\)', r'config.get(\1, default_value)', code)
        elif 'os.environ.get(' in code:
            # Add environment variable validation
            return re.sub(r'os\.environ\.get\((.*?)\)', r'get_validated_env(\1)', code)
        return code

    def _fix_security_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for security errors."""
        if 'password' in code:
            # Add password hashing
            return code.replace('password', 'hashed_password')
        elif 'token' in code:
            # Add secure token handling
            return code.replace('token', 'secure_token')
        return code

    def _fix_network_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for network errors."""
        if 'requests.get(' in code:
            # Add timeout and retry
            return re.sub(r'requests\.get\((.*?)\)', r'requests.get(\1, timeout=30, retries=3)', code)
        elif 'socket' in code:
            # Add connection error handling
            return f"""try:
    {code}
except ConnectionError as e:
    logger.error(f"Connection error: {e}")
    raise"""
        return code

    def _fix_filesystem_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for filesystem errors."""
        if 'open(' in code:
            # Add proper file handling
            return f"""with open({code.split('open(')[1].split(')')[0]}, 'r') as f:
    content = f.read()"""
        elif 'os.path' in code:
            # Add path existence check
            return f"""if os.path.exists({code.split('os.path.')[1].split('(')[1].split(')')[0]}):
    {code}"""
        return code

    def _fix_serialization_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for serialization errors."""
        if 'json.dumps(' in code:
            # Add proper serialization
            return code.replace('json.dumps(', 'json.dumps(, default=str)')
        elif 'pickle.dumps(' in code:
            # Add secure serialization
            return code.replace('pickle.dumps(', 'secure_pickle.dumps(')
        return code
    
    def _fix_generic_error(self, code: str, context: Dict[str, str]) -> str:
        """Generate fix for generic errors."""
        if 'try:' in code:
            # Add better error handling
            return code.replace('except Exception as e:', 'except Exception as e:\n    logger.error(f"Error: {str(e)}")\n    raise')
        return code
    
    def run(self):
        """Run the code fixer and print suggestions."""
        try:
            suggestions = self.suggest_code_changes()
            
            print("\nSuggested Code Changes:")
            print("=" * 80)
            
            for change in suggestions:
                print(f"\nFile: {change.file_path}")
                print(f"Line: {change.line_number}")
                print(f"Author: {change.author} (commit: {change.commit_hash})")
                print(f"Description: {change.description}")
                print("\nOriginal Code:")
                print(f"  {change.original_code}")
                print("\nSuggested Change:")
                print(f"  {change.new_code}")
                print("-" * 80)
            
        except Exception as e:
            logger.error(f"Error generating code changes: {e}")
            raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python code_fixer.py <issue_file>")
        sys.exit(1)
    
    fixer = CodeFixer(sys.argv[1])
    fixer.run() 