"""
Main entry point for the Autonomous App-Writing Agent.
"""

import threading
from autonomous_app_writer.core.logging_setup import setup_logging, get_logger
from autonomous_app_writer.vsm_daemons.system4_intelligence_daemon import System4IntelligenceDaemon
from autonomous_app_writer.vsm_daemons.system5_policy_daemon import System5PolicyDaemon
from autonomous_app_writer.vsm_system3_operations.project_lifecycle_manager import ProjectLifecycleManager

# --- Agent Initialization ---

def initialize_agent():
    """
    Initializes all agent components, including daemons and S1 agents.
    """
    setup_logging()
    logger = get_logger(__name__)
    logger.info("--- AUTONOMOUS APP-WRITING AGENT INITIALIZING ---")

    # Initialize all S1 agents so they register with the AgentState
    # In a real app, this might be done more dynamically.
    from autonomous_app_writer.vsm_system1_operational_agents import (
        RequirementsAgent, ArchitectureAgent, UiUxAgent, FrontendCoderAgent,
        BackendCoderAgent, DatabaseAgent, UnitTesterAgent, IntegrationTesterAgent,
        E2ETesterAgent, DeploymentAgent, DocumentationAgent, VersionControlAgent
    )
    RequirementsAgent()
    ArchitectureAgent()
    UiUxAgent()
    FrontendCoderAgent()
    BackendCoderAgent()
    DatabaseAgent()
    UnitTesterAgent()
    IntegrationTesterAgent()
    E2ETesterAgent()
    DeploymentAgent()
    DocumentationAgent()
    VersionControlAgent()

    # Start background daemons
    s4_daemon = System4IntelligenceDaemon()
    s5_daemon = System5PolicyDaemon()

    s4_thread = threading.Thread(target=s4_daemon.run, daemon=True)
    s5_thread = threading.Thread(target=s5_daemon.run, daemon=True)

    s4_thread.start()
    s5_thread.start()
    
    logger.info("--- AGENT INITIALIZATION COMPLETE. READY FOR REQUESTS. ---")

def handle_development_request(user_request):
    """
    Handles a single user request to develop an application.
    """
    logger = get_logger(__name__)
    logger.info(f"Received new development request: '{user_request}'")
    
    # System 3 takes over for the specific project
    project_manager = ProjectLifecycleManager(user_request)
    result = project_manager.run()
    
    logger.info(f"Development request finished. Final state: {result}")
    return result

# --- Main Execution ---

if __name__ == '__main__':
    initialize_agent()
    
    print("\n" + "="*50)
    print("Autonomous App-Writing Agent is Initialized and Ready.")
    print("="*50 + "\n")

    # Example of a project queue for sequential execution
    project_queue = [
        "Create a simple command-line application in Python that acts as a calculator. It should be able to add, subtract, multiply, and divide.",
        "Develop a basic HTML webpage with a header, a main content area, and a footer.",
        "Write a Python script that fetches the current weather from a public API for a given city."
    ]

    for request in project_queue:
        handle_development_request(request)
        print("\n" + "="*50)
        print(f"Completed project: {request}")
        print("="*50 + "\n")
