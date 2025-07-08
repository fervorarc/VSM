"""
S1.Deployment & DevOps Agent
"""

from .base_s1_agent import BaseS1Agent
from autonomous_app_writer import config

class DeploymentAgent(BaseS1Agent):
    """
    Handles CI/CD pipeline setup, containerization (e.g., Docker),
    and deployment to target environments.
    """
    def __init__(self):
        super().__init__("DeploymentAgent")

    def execute_task(self, task_details, project_state):
        """
        Executes a deployment-related task.

        Args:
            task_details (dict): The specific task, e.g., "Generate Dockerfile".
            project_state (dict): The current project state.

        Returns:
            dict: A dictionary with the status and resulting artifact.
        """
        self.logger.info(f"Executing deployment task: {task_details.get('description')}")
        
        task_type = task_details.get("type")
        if task_type == "generate_dockerfile":
            return self._generate_dockerfile(task_details, project_state)
        elif task_type == "generate_ci_cd_script":
            return self._generate_ci_cd_script(task_details, project_state)
        else:
            return self._create_task_result("FAILURE", error_message=f"Unknown deployment task type: {task_type}")

    def _generate_dockerfile(self, task_details, project_state):
        """
        Generates a Dockerfile for the application.
        """
        self.logger.debug("Generating Dockerfile.")
        context = self.get_relevant_context(project_state)
        
        prompt = f"""
        You are the S1.DeploymentAgent. Your task is to generate a Dockerfile for the application.

        Project Context:
        - Architecture: {context.get('architecture')}
        - Technology Stack: {context.get('architecture', {}).get('technology_stack')}

        Based on the context, generate an efficient and secure multi-stage Dockerfile.
        Your output should be only the Dockerfile code block.
        """
        
        dockerfile = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)
        return self._create_task_result("SUCCESS", artifact={"filename": "Dockerfile", "content": dockerfile})

    def _generate_ci_cd_script(self, task_details, project_state):
        """
        Generates a CI/CD pipeline script (e.g., for GitHub Actions).
        """
        self.logger.debug("Generating CI/CD script.")
        context = self.get_relevant_context(project_state)
        
        prompt = f"""
        You are the S1.DeploymentAgent. Your task is to generate a CI/CD pipeline script.

        Project Context:
        - Architecture: {context.get('architecture')}
        - CI/CD Platform: {task_details.get("platform", "GitHub Actions")}

        Based on the context, generate a CI/CD script that builds, tests, and deploys the application.
        Your output should be only the YAML/script code block.
        """
        
        ci_cd_script = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)
        filename = ".github/workflows/main.yml" if task_details.get("platform", "GitHub Actions") == "GitHub Actions" else "ci_cd_script.yml"
        return self._create_task_result("SUCCESS", artifact={"filename": filename, "content": ci_cd_script})

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()

    deployment_agent = DeploymentAgent()
    
    mock_project_state = {
        "architecture": {
            "technology_stack": {"backend": "Python/Flask", "database": "PostgreSQL"}
        }
    }
    task = {"description": "Generate Dockerfile for the backend service.", "type": "generate_dockerfile"}

    result = deployment_agent.execute_task(task, mock_project_state)
    
    import json
    print(json.dumps(result, indent=4))
