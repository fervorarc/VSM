"""
Main entry point for the Autonomous App-Writing Agent.
"""

from autonomous_app_writer.core.logging_setup import setup_logging, get_logger
from autonomous_app_writer.workflows.app_development_main_flow import handle_autonomous_app_development_request

def main():
    """
    Main function to initialize and run the agent.
    """
    setup_logging()
    logger = get_logger(__name__)
    logger.info("AUTONOMOUS APP-WRITING AGENT INITIALIZING...")

    # This is a placeholder for a user request.
    # In a real application, this would come from a UI, API, or CLI.
    user_request = {
        "description": "Create a simple Python script that prints 'Hello, World!'",
        "user_id": "mvp_user"
    }

    logger.info(f"Received user request: {user_request['description']}")

    app_result = handle_autonomous_app_development_request(user_request)
    logger.info(f"App development finished with result: {app_result}")

    logger.info("AGENT SHUTDOWN.")

if __name__ == "__main__":
    main()
