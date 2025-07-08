"""
S1.BackendCoding Agent
"""

from .base_coding_agent import BaseCodingAgent
from autonomous_app_writer import config

class BackendCoderAgent(BaseCodingAgent):
    """
    Implements server-side logic, business rules, API endpoints,
    and database interactions.
    """
    def __init__(self):
        super().__init__("BackendCoderAgent")

    def _generate_code(self, task_details, project_state):
        """
        Generates the initial block of backend code.
        """
        self.logger.debug(f"Generating backend code for task: {task_details.get('description')}")
        
        context = self.get_relevant_context(project_state)
        
        prompt = f"""
        You are the S1.BackendCoding Agent. Your task is to write backend code.

        Task: {task_details.get('description')}
        
        Project Context:
        - Architecture: {context.get('architecture')}
        - Technology Stack: {context.get('architecture', {}).get('technology_stack', {}).get('backend')}
        - API Contracts / Coordination Info: (Assume this would be passed in a real system)

        Based on the context, write the code for the specified backend feature (e.g., API endpoint).
        Ensure the code is secure and performant.
        Your output should be only the code block for the specified file/module.
        """
        
        generated_code = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)
        return generated_code

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()

    backend_agent = BackendCoderAgent()
    
    mock_project_state = {
        "architecture": {
            "technology_stack": {"backend": "Python/Flask"},
            "component_breakdown": ["A REST API for managing notes."]
        }
    }
    task = {"description": "Implement a GET endpoint at /api/notes to retrieve all notes."}

    result = backend_agent.execute_task(task, mock_project_state)
    
    import json
    print(json.dumps(result, indent=4))
