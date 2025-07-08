'''
Manages the global state of the agent, including S5 policies and S4 knowledge.

This module provides singleton-like access to the core state stores, ensuring that
all parts of the agent are working with the same information and policies.
'''

import threading
from autonomous_app_writer.core.logging_setup import get_logger

logger = get_logger(__name__)

class S5_Policy_Store:
    """A singleton store for System 5 policies."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(S5_Policy_Store, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.policies = {
            "agent_mission": "Autonomously create robust, user-centric applications.",
            "ethical_guidelines": [
                "Prioritize user data privacy.",
                "Ensure security standards are met.",
                "Avoid generating harmful or malicious code."
            ],
            "development_philosophy": {
                "maintainability": "high",
                "component_sourcing": "prefer open-source",
                "testing_level": "comprehensive"
            }
        }
        self._initialized = True
        logger.info("S5 Policy Store initialized with default policies.")

    def get_policy(self, key: str):
        return self.policies.get(key)

    def update_policy(self, key: str, value):
        logger.info(f"S5 Policy Update: {key} updated.")
        self.policies[key] = value

class S4_Environmental_Knowledge:
    """A singleton store for System 4 environmental knowledge."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(S4_Environmental_Knowledge, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.knowledge = {
            "tech_trends": {
                "frontend": "React with TypeScript",
                "backend": "Python with FastAPI",
                "database": "PostgreSQL"
            },
            "security_threats": [
                "Log4Shell vulnerability",
                "SQL Injection"
            ],
            "ux_ui_trends": [
                "Dark Mode",
                "Neumorphism"
            ]
        }
        self._initialized = True
        logger.info("S4 Environmental Knowledge initialized with default data.")

    def get_knowledge(self, key: str):
        return self.knowledge.get(key)

    def update_knowledge(self, key: str, value):
        logger.info(f"S4 Knowledge Update: {key} updated.")
        self.knowledge[key] = value

# Instantiate the singletons for global access
policy_store = S5_Policy_Store()
environmental_knowledge = S4_Environmental_Knowledge()
