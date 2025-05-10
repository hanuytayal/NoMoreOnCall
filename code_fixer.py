import json
import os
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeFixer:
    def __init__(self, issue_file: str):
        self.issue_file = issue_file
        self.issue_data = self._load_issue_file()

    def _load_issue_file(self) -> Dict:
        with open(self.issue_file, 'r') as f:
            return json.load(f)

    def suggest_code_changes(self) -> List[Dict]:
        """
        Suggest code changes based on the LLM analysis and code analysis sections.
        """
        suggestions = []
        llm = self.issue_data['llm_analysis']
        for file in self.issue_data['code_analysis']:
            for line in file['error_lines']:
                suggestions.append({
                    'file_path': file['file_path'],
                    'line_number': line['line_number'],
                    'current_code': line['code'],
                    'suggested_fix': llm['suggested_fixes'],
                    'reason': llm['root_cause']
                })
        return suggestions

    def create_pr_description(self, suggestions: List[Dict]) -> str:
        llm = self.issue_data['llm_analysis']
        error = self.issue_data['error_details']
        desc = f"""
### Fix for {error['type']} ({error['id']})

**Root Cause:** {llm['root_cause']}

**Explanation:** {llm['explanation']}

**Suggested Fixes:** {llm['suggested_fixes']}

**Prevention:** {llm['prevention']}

#### Code Changes:
"""
        for s in suggestions:
            desc += f"\n- `{s['file_path']}` line {s['line_number']}:\n  - Current: `{s['current_code']}`\n  - Suggestion: {s['suggested_fix']}\n  - Reason: {s['reason']}\n"
        return desc

    def run(self):
        suggestions = self.suggest_code_changes()
        pr_desc = self.create_pr_description(suggestions)
        print("\n===== CODE FIX SUGGESTIONS =====\n")
        for s in suggestions:
            print(f"File: {s['file_path']} | Line: {s['line_number']}\n  Current: {s['current_code']}\n  Suggestion: {s['suggested_fix']}\n  Reason: {s['reason']}\n")
        print("\n===== PR DESCRIPTION =====\n")
        print(pr_desc)

if __name__ == "__main__":
    fixer = CodeFixer("issue_ERR_123.json")
    fixer.run() 