"""
S1.RequirementsElicitation & Clarification Agent
"""

from .base_s1_agent import BaseS1Agent
from autonomous_app_writer import config

class RequirementsAgent(BaseS1Agent):
    """
    Interacts with the user to understand, clarify, and structure application requirements.
    """
    def __init__(self):
        super().__init__("RequirementsAgent")

    def execute_task(self, task_details, project_state):
        """
        Executes the requirements elicitation task. This version simulates a multi-turn dialogue.
        """
        self.logger.info("Executing requirements elicitation task.")
        user_prompt = task_details.get("user_prompt")
        if not user_prompt:
            return self._create_task_result("FAILURE", error_message="User prompt is missing.")

        conversation_history = [f"User: {user_prompt}"]
        
        # Simulate a multi-turn conversation for clarification
        for i in range(2): # Simulate 2 turns of clarification
            self.logger.info(f"Requirements clarification, turn {i+1}")
            prompt = f"""
            You are a requirements analyst. Based on the conversation so far,
            ask one single, critical question to clarify the user's needs.
            If you have enough information, instead respond with "DONE".

            Conversation History:
            {conversation_history}
            """
            question = self.llm_service.generate_text(prompt, model=config.DEFAULT_FAST_MODEL)
            
            if "DONE" in question.upper():
                break
            
            conversation_history.append(f"Agent: {question}")
            # In a real system, we would get user input here. We'll simulate it.
            simulated_answer = self.llm_service.generate_text(f"Answer this question: {question}")
            conversation_history.append(f"User (simulated): {simulated_answer}")

        # Final call to structure the requirements
        conversation_str = "\n".join(conversation_history)
        final_prompt = f"""
        You are the S1.RequirementsElicitation Agent. Based on the following conversation,
        convert the user's request into a structured, machine-readable format.

        Conversation History:
        {conversation_str}

        Core Policies:
        {self.agent_state.s5_policies}

        Output the result as a JSON object with keys for "functional_requirements", 
        "non_functional_requirements", and "user_personas".
        """

        response_str = self.llm_service.generate_text(final_prompt, model=config.DEFAULT_MAIN_MODEL)

        try:
            structured_requirements = self.llm_service.parse_json_response(response_str)
            self.logger.info("Successfully structured user requirements after clarification.")
            return self._create_task_result("SUCCESS", artifact=structured_requirements)
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response for requirements: {e}")
            return self._create_task_result("FAILURE", error_message=f"LLM response parsing failed: {e}")

# Example of how to instantiate and use the agent
if __name__ == '__main__':
    # This setup is for standalone testing of the agent.
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()
    
    req_agent = RequirementsAgent()
    task = {"user_prompt": "I want a simple, secure mobile app to track my daily water intake."}
    result = req_agent.execute_task(task, {})
    
    import json
    print(json.dumps(result, indent=4))
