"""
S1.DatabaseManagement Agent
"""

from .base_coding_agent import BaseCodingAgent
from autonomous_app_writer import config

class DatabaseAgent(BaseCodingAgent):
    """
    Designs database schemas and generates/manages database migration scripts.
    """
    def __init__(self):
        super().__init__("DatabaseAgent")

    def _generate_code(self, task_details, project_state):
        """
        Generates a database schema or migration script.
        """
        self.logger.debug(f"Generating database artifact for task: {task_details.get('description')}")
        
        context = self.get_relevant_context(project_state)
        
        prompt = f"""
        You are the S1.DatabaseManagement Agent. Your task is to design a database schema
        or write a migration script.

        Task: {task_details.get('description')}
        
        Project Context:
        - Requirements: {context.get('requirements')}
        - Architecture: {context.get('architecture')}
        - Technology Stack: {context.get('architecture', {}).get('technology_stack', {}).get('database')}

        Based on the context, generate the appropriate SQL DDL, schema definition, or migration script.
        Your output should be only the code block.
        """
        
        generated_code = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)
        return generated_code

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()

    db_agent = DatabaseAgent()
    
    mock_project_state = {
        "requirements": {
            "functional_requirements": ["A user has a username and a hashed password."]
        },
        "architecture": {
            "technology_stack": {"database": "PostgreSQL"}
        }
    }
    task = {"description": "Create the 'users' table schema."}

    result = db_agent.execute_task(task, mock_project_state)
    
    import json
    print(json.dumps(result, indent=4))
