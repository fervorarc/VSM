"""
S1.FrontendCoding Agent
"""

from .base_coding_agent import BaseCodingAgent
from autonomous_app_writer import config

class FrontendCoderAgent(BaseCodingAgent):
    """
    Takes UI/UX designs, architectural specs, and API contracts
    to write frontend code (e.g., HTML, CSS, JavaScript, React).
    """
    def __init__(self):
        super().__init__("FrontendCoderAgent")

    def _generate_code(self, task_details, project_state):
        """
        Generates the initial block of frontend code.
        """
        self.logger.debug(f"Generating frontend code for task: {task_details.get('description')}")
        
        context = self.get_relevant_context(project_state)
        
        prompt = f"""
        You are the S1.FrontendCoding Agent. Your task is to write frontend code.

        Task: {task_details.get('description')}
        
        Project Context:
        - UI/UX Design: {context.get('ui_ux_design')}
        - Architecture: {context.get('architecture')}
        - Technology Stack: {context.get('architecture', {}).get('technology_stack', {}).get('frontend')}

        Based on the context, write the code for the specified frontend component or feature.
        Your output should be only the code block for the specified file/component.
        """
        
        # This is a simplified generation step. A real system would be more specific
        # about file names, dependencies, etc.
        generated_code = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)
        return generated_code

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()

    frontend_agent = FrontendCoderAgent()
    
    mock_project_state = {
        "ui_ux_design": {
            "wireframes": ["A login screen with email and password fields, and a submit button."]
        },
        "architecture": {
            "technology_stack": {"frontend": "HTML/CSS/JavaScript"}
        }
    }
    task = {"description": "Create the HTML structure for the login page."}

    result = frontend_agent.execute_task(task, mock_project_state)
    
    import json
    print(json.dumps(result, indent=4))
