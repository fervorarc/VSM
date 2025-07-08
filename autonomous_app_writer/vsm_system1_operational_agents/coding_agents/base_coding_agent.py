"""
Base class for all S1 coding agents.
"""

from ..base_s1_agent import BaseS1Agent
from autonomous_app_writer import config

class BaseCodingAgent(BaseS1Agent):
    """
    An abstract base class for agents that write code.
    Provides a common structure for code generation, self-critique, and testing.
    """
    def __init__(self, agent_name):
        super().__init__(agent_name)

    def execute_task(self, task_details, project_state):
        """
        Main entry point for a coding task.

        Args:
            task_details (dict): The specific coding task (e.g., "Implement login API endpoint").
            project_state (dict): The overall project state.

        Returns:
            dict: A result dictionary with status and the generated code artifact.
        """
        self.logger.info(f"Executing coding task: {task_details.get('description')}")

        # 1. Generate Code
        generated_code = self._generate_code(task_details, project_state)
        if not generated_code:
            return self._create_task_result("FAILURE", error_message="Code generation failed.")

        # 2. Self-Critique and Refine (could be a loop)
        refined_code = self._self_critique_and_refine(generated_code, task_details, project_state)
        if not refined_code:
            return self._create_task_result("FAILURE", error_message="Code refinement failed.")

        # 3. Run Local Tests (e.g., linting, unit tests)
        tests_passed = self._run_local_tests(refined_code, task_details)
        if not tests_passed:
            # In a more complex system, this could trigger a debugging loop.
            return self._create_task_result("FAILURE", error_message="Local tests failed.")

        self.logger.info("Coding task completed successfully.")
        
        # Commit the successful code
        vcs_agent = self.agent_state.get_s1_agent("VersionControlAgent")
        if vcs_agent:
            commit_task = {
                "action": "commit",
                "message": f"feat: Implement task '{task_details.get('description')}'",
                "files_to_add": ["."] # Simple for now
            }
            vcs_agent.execute_task(commit_task, project_state)

        return self._create_task_result("SUCCESS", artifact={"code": refined_code, "task": task_details, "filename": f"{self.agent_name.lower()}_output.py"})

    def _generate_code(self, task_details, project_state):
        """
        Generates the initial block of code. To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _generate_code")

    def _self_critique_and_refine(self, code, task_details, project_state):
        """
        Uses an LLM to critique and refine the generated code.
        """
        self.logger.debug("Performing self-critique on generated code.")
        context = self.get_relevant_context(project_state)
        
        prompt = f"""
        You are a code reviewer. Critique the following code based on the task requirements,
        architectural design, and coding best practices from the agent's policies.

        Task: {task_details.get('description')}
        Architecture: {context.get('architecture')}
        Policies: {context.get('policies')['development_philosophy']}
        
        Code to review:
        ```
        {code}
        ```

        Provide feedback and the refined code. If the code is good, return it as is.
        Your output should be only the refined code block.
        """
        
        refined_code = self.llm_service.generate_text(prompt, model=config.DEFAULT_FAST_MODEL)
        return refined_code

    def _run_local_tests(self, code, task_details):
        """
        Runs local tests like linters or unit tests.
        This is a placeholder for more specific testing logic.
        """
        self.logger.debug("Running local tests on the code.")
        # In a real implementation, you would save the code to a temporary file
        # and then run a tool like a linter.
        # For example:
        # with open("temp_file.py", "w") as f:
        #     f.write(code)
        # result = self.tool_interface.run_linter("temp_file.py")
        # return result['return_code'] == 0
        
        # Placeholder returns True
        return True
