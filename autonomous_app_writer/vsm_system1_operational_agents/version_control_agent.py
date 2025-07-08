"""
S1.VersionControl Agent
"""

from .base_s1_agent import BaseS1Agent

class VersionControlAgent(BaseS1Agent):
    """
    Interacts with version control systems (e.g., Git). Manages commits,
    branching strategies, and merging as directed by S3.
    """
    def __init__(self):
        super().__init__("VersionControlAgent")

    def execute_task(self, task_details, project_state):
        """
        Executes a version control task.

        Args:
            task_details (dict): The specific task, e.g., {"action": "commit", "message": "..."}.
            project_state (dict): The current project state.

        Returns:
            dict: A dictionary with the status of the operation.
        """
        self.logger.info(f"Executing version control task: {task_details}")
        
        action = task_details.get("action")
        project_path = project_state.get("project_path") # Assumes S3 provides this

        if not project_path:
            return self._create_task_result("FAILURE", error_message="Project path not specified.")

        if action == "initialize":
            return self._initialize_repo(project_path)
        elif action == "commit":
            return self._commit_changes(project_path, task_details.get("message"), task_details.get("files_to_add", ["."]))
        else:
            return self._create_task_result("FAILURE", error_message=f"Unknown VCS action: {action}")

    def _initialize_repo(self, project_path):
        """Initializes a new Git repository."""
        self.logger.info(f"Initializing Git repository at {project_path}")
        command = f"cd {project_path} && git init"
        result = self.tool_interface.execute_shell_command(command)
        if result['return_code'] == 0:
            return self._create_task_result("SUCCESS", artifact=result['stdout'])
        else:
            return self._create_task_result("FAILURE", error_message=result['stderr'])

    def _commit_changes(self, project_path, commit_message, files_to_add):
        """Adds and commits changes to the repository."""
        if not commit_message:
            return self._create_task_result("FAILURE", error_message="Commit message cannot be empty.")
        
        files_str = " ".join(files_to_add)
        self.logger.info(f"Committing changes in {project_path} with message: '{commit_message}'")
        
        add_command = f"cd {project_path} && git add {files_str}"
        add_result = self.tool_interface.execute_shell_command(add_command)
        if add_result['return_code'] != 0:
            return self._create_task_result("FAILURE", error_message=f"git add failed: {add_result['stderr']}")

        commit_command = f"cd {project_path} && git commit -m \"{commit_message}\""
        commit_result = self.tool_interface.execute_shell_command(commit_command)
        if commit_result['return_code'] == 0:
            return self._create_task_result("SUCCESS", artifact=commit_result['stdout'])
        else:
            return self._create_task_result("FAILURE", error_message=f"git commit failed: {commit_result['stderr']}")

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    import os
    setup_logging()

    vcs_agent = VersionControlAgent()
    
    # Create a dummy project directory for testing
    test_dir = "temp_test_project"
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, "test.txt"), "w") as f:
        f.write("hello")

    mock_state = {"project_path": test_dir}
    init_task = {"action": "initialize"}
    commit_task = {"action": "commit", "message": "Initial commit"}

    vcs_agent.execute_task(init_task, mock_state)
    result = vcs_agent.execute_task(commit_task, mock_state)
    
    import json
    print(json.dumps(result, indent=4))

    # Clean up
    import shutil
    shutil.rmtree(test_dir)
