"""
Abstract Base Class for all VSM System 1 (S1) Operational Agents.
"""

from abc import ABC, abstractmethod
from autonomous_app_writer.core.logging_setup import get_logger
from autonomous_app_writer.core.llm_services import get_llm_service
from autonomous_app_writer.core.tool_interface import get_tool_interface
from autonomous_app_writer.core.agent_state import get_agent_state

class BaseS1Agent(ABC):
    """
    A base class for all S1 agents, providing common functionalities.
    """
    def __init__(self, agent_name):
        """
        Initializes the base agent.

        Args:
            agent_name (str): The name of the agent (e.g., "RequirementsAgent").
        """
        self.agent_name = agent_name
        self.logger = get_logger(f"S1.{self.agent_name}")
        self.llm_service = get_llm_service()
        self.tool_interface = get_tool_interface()
        self.agent_state = get_agent_state()
        
        # Register the agent instance with the global state
        self.agent_state.register_s1_capability(self.agent_name, self)
        self.logger.info(f"S1 Agent '{self.agent_name}' initialized and registered.")

    @abstractmethod
    def execute_task(self, task_details, project_state):
        """
        The main entry point for an agent to perform its task.
        This method must be implemented by all concrete S1 agent classes.

        Args:
            task_details (dict): A dictionary containing the specifics of the task.
            project_state (object): The current state of the entire project, providing context.

        Returns:
            dict: A dictionary containing the status of the task ('SUCCESS' or 'FAILURE'),
                  any resulting artifacts, and an optional error message.
        """
        pass

    def get_relevant_context(self, project_state):
        """
        Helper method to extract relevant context for prompting the LLM.
        Can be overridden by subclasses for more specific context gathering.
        """
        return {
            "requirements": project_state.get("structured_requirements"),
            "architecture": project_state.get("architecture_design"),
            "ui_ux_design": project_state.get("ui_ux_design"),
            "policies": self.agent_state.s5_policies,
            "s4_knowledge": self.agent_state.s4_knowledge
        }

    def _create_task_result(self, status, artifact=None, error_message=None):
        """
        A standardized way to create the return dictionary for execute_task.
        """
        return {
            "status": status,
            "artifact": artifact,
            "error": error_message
        }
