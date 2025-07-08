"""
Base class for all S1 testing agents.
"""

from ..base_s1_agent import BaseS1Agent

class BaseTestingAgent(BaseS1Agent):
    """
    An abstract base class for agents that perform testing tasks.
    """
    def __init__(self, agent_name):
        super().__init__(agent_name)

    def execute_task(self, task_details, project_state):
        """
        Main entry point for a testing task.

        Args:
            task_details (dict): The specific testing task.
            project_state (dict): The overall project state.

        Returns:
            dict: A result dictionary with status and a test report.
        """
        self.logger.info(f"Executing testing task: {task_details.get('description')}")

        # 1. Generate Test Cases
        test_cases = self._generate_test_cases(task_details, project_state)
        if not test_cases:
            return self._create_task_result("FAILURE", error_message="Test case generation failed.")

        # 2. Execute Tests
        test_results = self._execute_tests(test_cases, project_state)
        if not test_results:
            return self._create_task_result("FAILURE", error_message="Test execution failed.")

        # 3. Generate Report
        report = self._generate_report(test_results)

        self.logger.info("Testing task completed successfully.")
        return self._create_task_result("SUCCESS", artifact=report)

    def _generate_test_cases(self, task_details, project_state):
        """
        Generates test cases. To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _generate_test_cases")

    def _execute_tests(self, test_cases, project_state):
        """
        Executes the generated test cases. To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _execute_tests")

    def _generate_report(self, test_results):
        """
        Generates a standardized test report from the results.
        """
        self.logger.debug("Generating test report.")
        # This is a simplified report. A real system might include more details.
        passed_count = sum(1 for result in test_results if result['status'] == 'PASS')
        failed_count = len(test_results) - passed_count
        
        return {
            "summary": {
                "total_tests": len(test_results),
                "passed": passed_count,
                "failed": failed_count
            },
            "details": test_results
        }
