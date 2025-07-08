"""
S1.UI/UXDesign Agent
"""

from .base_s1_agent import BaseS1Agent
from autonomous_app_writer import config

class UiUxAgent(BaseS1Agent):
    """
    Generates UI wireframes, mockups, and user flows based on
    requirements and user personas.
    """
    def __init__(self):
        super().__init__("UiUxAgent")

    def execute_task(self, task_details, project_state):
        """
        Executes the UI/UX design task.

        Args:
            task_details (dict): Can be empty, required info is in project_state.
            project_state (dict): The current project state.

        Returns:
            dict: A dictionary with the UI/UX design assets.
        """
        self.logger.info("Executing UI/UX design task.")
        
        structured_requirements = project_state.get("structured_requirements")
        if not structured_requirements:
            return self._create_task_result("FAILURE", error_message="Structured requirements not found.")

        context = self.get_relevant_context(project_state)

        prompt = f"""
        You are the S1.UI/UXDesign Agent. Your task is to design the user interface
        and experience for an application.

        Structured Requirements:
        {structured_requirements}

        Relevant Context (Policies & S4 UX/UI Trends):
        {context['policies']}
        {context['s4_knowledge'].get('ux_ui_trends')}

        Based on this, generate a description of the UI/UX design.
        Your output must be a JSON object with the following keys:
        - "color_palette": A dictionary with primary, secondary, and accent colors.
        - "typography": A dictionary with font families for headings and body text.
        - "user_flows": A dictionary describing key user journeys (e.g., "login_flow", "onboarding_flow").
        - "wireframes": A list of text-based descriptions of wireframes for major screens.
        """

        response_str = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)

        try:
            ui_ux_design = self.llm_service.parse_json_response(response_str) # Assumes such a method exists
            self.logger.info("Successfully designed the UI/UX.")
            return self._create_task_result("SUCCESS", artifact=ui_ux_design)
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response for UI/UX design: {e}")
            return self._create_task_result("FAILURE", error_message=f"LLM response parsing failed: {e}")

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()

    ui_agent = UiUxAgent()
    
    mock_project_state = {
        "structured_requirements": {
            "user_personas": ["A busy professional who needs to quickly add notes."],
            "functional_requirements": ["User can create, view, and delete notes."],
            "non_functional_requirements": ["The app should have a clean, minimalist interface."]
        },
        "s4_knowledge": {
            "ux_ui_trends": ["Minimalism", "Dark mode support"]
        }
    }

    result = ui_agent.execute_task({}, mock_project_state)
    
    import json
    print(json.dumps(result, indent=4))
