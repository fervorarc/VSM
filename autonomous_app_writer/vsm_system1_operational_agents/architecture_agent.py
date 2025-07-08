"""
S1.ArchitectureDesign Agent
"""

from .base_s1_agent import BaseS1Agent
from autonomous_app_writer import config

class ArchitectureAgent(BaseS1Agent):
    """
    Proposes a suitable software architecture, technology stack,
    and major component breakdown based on requirements.
    """
    def __init__(self):
        super().__init__("ArchitectureAgent")

    def execute_task(self, task_details, project_state):
        """
        Executes the architecture design task.

        Args:
            task_details (dict): This can be empty, as the required info is in project_state.
            project_state (dict): The current state of the project, containing structured_requirements.

        Returns:
            dict: A dictionary with the architecture design document.
        """
        self.logger.info("Executing architecture design task.")
        
        structured_requirements = project_state.get("structured_requirements")
        if not structured_requirements:
            return self._create_task_result("FAILURE", error_message="Structured requirements not found in project state.")

        context = self.get_relevant_context(project_state)

        prompt = f"""
        You are the S1.ArchitectureDesign Agent. Your task is to design the software architecture
        for an application based on the provided requirements and environmental knowledge.

        Structured Requirements:
        {structured_requirements}

        Relevant Context (Policies & Environmental Knowledge):
        {context['policies']}
        {context['s4_knowledge']}

        Based on all this information, propose a suitable software architecture.
        Your output must be a JSON object with the following keys:
        - "architecture_pattern": (e.g., "Microservices", "Monolithic", "Serverless").
        - "technology_stack": A dictionary with keys like "frontend", "backend", "database".
        - "component_breakdown": A list of major components and their responsibilities.
        - "design_rationale": A brief explanation for your choices.
        """

        response_str = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)

        try:
            architecture_design = self.llm_service.parse_json_response(response_str) # Assumes such a method exists
            self.logger.info("Successfully designed the software architecture.")
            return self._create_task_result("SUCCESS", artifact=architecture_design)
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response for architecture design: {e}")
            return self._create_task_result("FAILURE", error_message=f"LLM response parsing failed: {e}")

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()

    arch_agent = ArchitectureAgent()
    
    # Mock project state
    mock_project_state = {
        "structured_requirements": {
            "functional_requirements": [
                "User can register and log in.",
                "User can create, view, and delete notes."
            ],
            "non_functional_requirements": [
                "The application must be a web app accessible from modern browsers.",
                "Must be secure and prevent common web vulnerabilities."
            ]
        }
    }

    result = arch_agent.execute_task({}, mock_project_state)
    
    import json
    print(json.dumps(result, indent=4))
