"""
S1.Documentation Agent
"""

from .base_s1_agent import BaseS1Agent
from autonomous_app_writer import config

class DocumentationAgent(BaseS1Agent):
    """
    Automatically generates technical documentation from code, design documents,
    and architectural diagrams.
    """
    def __init__(self):
        super().__init__("DocumentationAgent")

    def execute_task(self, task_details, project_state):
        """
        Executes the documentation generation task.

        Args:
            task_details (dict): The specific documentation task.
            project_state (dict): The current project state.

        Returns:
            dict: A dictionary with the generated documentation.
        """
        self.logger.info(f"Executing documentation task: {task_details.get('description')}")
        
        context = self.get_relevant_context(project_state)
        
        prompt = f"""
        You are the S1.DocumentationAgent. Your task is to generate comprehensive
        technical documentation for the application.

        Project Context:
        - Requirements: {context.get('requirements')}
        - Architecture: {context.get('architecture')}
        - UI/UX Design: {context.get('ui_ux_design')}
        - Code Artifacts: (Summary or list of files would be provided here)

        Based on all available information, generate a README.md file for the project.
        The README should include:
        - A project overview.
        - A description of the architecture and technology stack.
        - Instructions on how to set up and run the project.
        - An overview of the main features.

        Your output should be only the Markdown content for the README.md file.
        """
        
        readme_content = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)
        
        return self._create_task_result("SUCCESS", artifact={"filename": "README.md", "content": readme_content})

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()

    doc_agent = DocumentationAgent()
    
    mock_project_state = {
        "requirements": {"functional_requirements": ["User can log in."]},
        "architecture": {"technology_stack": {"frontend": "React", "backend": "Node.js"}},
        "ui_ux_design": {"user_flows": {"login_flow": "..."}}
    }
    task = {"description": "Generate the project README file."}

    result = doc_agent.execute_task(task, mock_project_state)
    
    import json
    print(json.dumps(result, indent=4))
