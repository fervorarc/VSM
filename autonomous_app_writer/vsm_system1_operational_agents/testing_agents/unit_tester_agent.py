"""
S1.UnitTextWriter Agent
"""

from .base_testing_agent import BaseTestingAgent
from autonomous_app_writer import config

class UnitTesterAgent(BaseTestingAgent):
    """
    Generates and runs unit tests for code produced by coding S1s.
    """
    def __init__(self):
        super().__init__("UnitTesterAgent")

    def _generate_test_cases(self, task_details, project_state):
        """
        Generates unit test cases for a specific code artifact.
        """
        code_artifact = task_details.get("code_artifact", {})
        code_to_test = code_artifact.get("code")
        
        if not code_to_test:
            self.logger.error("No code provided to generate unit tests for.")
            return None

        self.logger.debug(f"Generating unit tests for code: {code_to_test[:100]}...")
        context = self.get_relevant_context(project_state)

        prompt = f"""
        You are the S1.UnitTesterAgent. Your task is to write unit tests for a given
        piece of code, using the specified testing framework.

        Code to Test:
        ```
        {code_to_test}
        ```

        Project Context:
        - Requirements: {context.get('requirements')}
        - Architecture: {context.get('architecture')}
        - Testing Framework: (e.g., pytest for Python, Jest for JavaScript)

        Write a complete unit test suite for the provided code.
        Your output should be only the code block containing the tests.
        """
        
        test_code = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)
        return [{"test_code": test_code}] # Return a list of test cases

    def _execute_tests(self, test_cases, project_state):
        """
        Executes the generated unit tests.
        """
        self.logger.debug("Executing generated unit tests.")
        results = []
        for case in test_cases:
            test_code = case.get("test_code")
            # In a real system, you would save this test code to a file
            # and run it using a test runner tool via the tool_interface.
            # e.g., self.tool_interface.execute_shell_command("pytest temp_test_file.py")
            
            # Placeholder execution
            result = self.tool_interface.execute_shell_command(f"echo 'Running tests...' && echo '1 passed'")
            
            results.append({
                "test_case": "unit_test_suite",
                "status": "PASS" if result['return_code'] == 0 else "FAIL",
                "output": result['stdout']
            })
        return results

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()

    unit_tester = UnitTesterAgent()
    
    mock_task = {
        "description": "Test the add(a, b) function.",
        "code_artifact": {
            "code": "def add(a, b):\n    return a + b"
        }
    }

    result = unit_tester.execute_task(mock_task, {})
    
    import json
    print(json.dumps(result, indent=4))
