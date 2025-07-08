"""
Manages the global state of the agent.
This includes S5 Policies, S4 Knowledge, and S1 Capabilities.
"""

import json
import os
from autonomous_app_writer import config
from autonomous_app_writer.core.logging_setup import get_logger

logger = get_logger(__name__)

class AgentState:
    """
    A singleton class to manage the agent's state.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentState, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.s5_policies = {}
        self.s4_knowledge = {}
        self.s1_capabilities = {}
        
        self._ensure_knowledge_base_dir()
        self.load_s5_policies()
        self.load_s4_knowledge()
        logger.info("AgentState initialized.")

    def _ensure_knowledge_base_dir(self):
        """Ensures the knowledge base directory exists."""
        os.makedirs(config.KNOWLEDGE_BASE_DIR, exist_ok=True)

    def load_s5_policies(self, file_path=config.S5_POLICY_FILE):
        """Loads S5 policies from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                self.s5_policies = json.load(f)
            logger.info(f"S5 policies loaded from {file_path}")
        except FileNotFoundError:
            logger.warning(f"S5 policy file not found at {file_path}. Using default policies.")
            self.s5_policies = self._get_default_policies()
            self.save_s5_policies()

    def save_s5_policies(self, file_path=config.S5_POLICY_FILE):
        """Saves S5 policies to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.s5_policies, f, indent=4)
        logger.info(f"S5 policies saved to {file_path}")

    def load_s4_knowledge(self, file_path=config.S4_KNOWLEDGE_FILE):
        """Loads S4 knowledge from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                self.s4_knowledge = json.load(f)
            logger.info(f"S4 knowledge loaded from {file_path}")
        except FileNotFoundError:
            logger.warning(f"S4 knowledge file not found at {file_path}. Initializing empty knowledge base.")
            self.s4_knowledge = {"tech_trends": [], "security_threats": [], "ux_ui_trends": []}
            self.save_s4_knowledge()

    def save_s4_knowledge(self, file_path=config.S4_KNOWLEDGE_FILE):
        """Saves S4 knowledge to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(self.s4_knowledge, f, indent=4)
        logger.info(f"S4 knowledge saved to {file_path}")

    def register_s1_capability(self, agent_name, agent_instance):
        """Registers an S1 agent's capabilities."""
        self.s1_capabilities[agent_name] = agent_instance
        logger.info(f"Registered S1 capability: {agent_name}")

    def get_s1_agent(self, agent_name):
        """Retrieves a registered S1 agent."""
        return self.s1_capabilities.get(agent_name)

    def _get_default_policies(self):
        """Returns a set of default S5 policies."""
        return {
            "agent_mission": "Autonomously create robust, user-centric applications.",
            "ethical_guidelines": {
                "data_privacy": "Prioritize user data privacy and security.",
                "responsible_ai": "Ensure transparency and fairness in AI use.",
                "security": "Adhere to high security standards (e.g., OWASP Top 10)."
            },
            "development_philosophy": {
                "code_maintainability": "Write clean, well-documented, and maintainable code.",
                "component_sourcing": "Favor well-maintained open-source components where appropriate.",
                "testing": "All code must have corresponding unit tests."
            },
            "success_criteria": "Deliver functional, tested, and documented applications that meet user requirements."
        }

# Singleton instance
agent_state = AgentState()

def get_agent_state():
    """Returns the singleton AgentState instance."""
    return agent_state
