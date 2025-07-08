"""
VSM System 2: Coordination and Conflict Resolution.
"""

from autonomous_app_writer.core.logging_setup import get_logger
from autonomous_app_writer.core.llm_services import get_llm_service

logger = get_logger(__name__)

class CoordinatorService:
    """
    Ensures smooth, stable, and harmonious interaction between S1 operational units.
    Resolves conflicts and standardizes communication protocols.
    """
    def __init__(self):
        self.llm_service = get_llm_service()
        logger.info("System 2 Coordinator Service initialized.")

    def get_s1_coordination_context(self, task, project_state):
        """
        Provides the necessary context for an S1 agent to perform its task,
        ensuring it has the required information from other S1s.

        Args:
            task (dict): The task to be executed.
            project_state (dict): The current state of the project.

        Returns:
            dict: A dictionary of context needed for the task.
        """
        logger.debug(f"S2: Providing coordination context for task: {task.get('description')}")
        
        # This is a simplified example. A real system would have more complex logic
        # to fetch specific dependencies, like API contracts from a backend task
        # for a frontend task.
        
        # For now, it just passes a reference to the whole project state.
        # S1 agents can then pull what they need.
        return {
            "project_state": project_state
        }

    def resolve_dependency_conflict(self, conflict_details):
        """
        Uses an LLM to mediate a conflict between S1 agents.

        Args:
            conflict_details (dict): Details of the conflict.

        Returns:
            str: A proposed resolution.
        """
        logger.warning(f"S2: Attempting to resolve dependency conflict: {conflict_details}")
        
        prompt = f"""
        You are the VSM System 2 Coordinator. There is a conflict between two
        operational agents. Your task is to propose a resolution.

        Conflict Details:
        {conflict_details}

        Propose a clear, actionable resolution to this conflict.
        """
        
        resolution = self.llm_service.generate_text(prompt)
        logger.info(f"S2: Proposed resolution: {resolution}")
        return resolution

# Singleton instance
coordinator_service = CoordinatorService()

def get_coordinator_service():
    """
    Returns the singleton CoordinatorService instance.
    """
    return coordinator_service
