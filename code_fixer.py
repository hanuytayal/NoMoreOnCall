import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any

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
                if self.issue_data['error_details']['type'] == 'DatabaseError':
                    new_code = self._fix_database_error(original_code)
                elif self.issue_data['error_details']['type'] == 'AuthenticationError':
                    new_code = self._fix_auth_error(original_code)
                else:
                    new_code = original_code  # No specific fix
                
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
    
    def _fix_database_error(self, code: str) -> str:
        """Generate fix for database errors."""
        if 'timeout=5' in code:
            return code.replace('timeout=5', 'timeout=30')
        return code
    
    def _fix_auth_error(self, code: str) -> str:
        """Generate fix for authentication errors."""
        if 'len(token) < 32' in code:
            return code.replace('len(token) < 32', 'not is_valid_token_format(token)')
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