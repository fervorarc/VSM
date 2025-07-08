"""
Central system for handling Algedonic Signals (pain/pleasure).
This is crucial for the agent's learning and adaptation mechanisms.
"""

from autonomous_app_writer.core.logging_setup import get_logger

logger = get_logger(__name__)

class AlgedonicManager:
    """
    Manages the routing and processing of algedonic signals.
    """
    def __init__(self):
        self.signal_queue = []
        logger.info("Algedonic Manager initialized.")

    def handle_signal(self, signal_type, event_category, details, target_systems=None):
        """
        Logs and routes a signal to the appropriate systems.

        Args:
            signal_type (str): "PAIN" or "PLEASURE".
            event_category (str): A descriptor for the event (e.g., "S1_Task_Failure").
            details (dict): A dictionary containing details about the event.
            target_systems (list, optional): A list of VSM systems to notify (e.g., ["S3", "S4"]).
        """
        log_level = "ERROR" if signal_type == "PAIN" else "INFO"
        
        logger.log(
            getattr(logger, log_level.lower()),
            f"ALGEDONIC SIGNAL ({signal_type}): Category='{event_category}', "
            f"Details={details}, Targets={target_systems or 'All'}"
        )

        # Here, you would add logic to route the signal to the actual system components.
        # For example, a critical PAIN signal might trigger a notification to a human overseer,
        # update a metric in a monitoring system, or directly influence the state of a
        # running workflow in S3 or S4.

        if target_systems:
            for system in target_systems:
                self._route_to_system(system, signal_type, event_category, details)
        
        # Add signal to the queue
        self.signal_queue.append({
            "type": signal_type,
            "category": event_category,
            "details": details,
            "target_systems": target_systems
        })

    def get_signals(self, clear_queue=True):
        """
        Retrieves all signals from the queue.
        
        Args:
            clear_queue (bool): If True, clears the queue after retrieving signals.

        Returns:
            list: A list of signal dictionaries.
        """
        signals = list(self.signal_queue)
        if clear_queue:
            self.signal_queue.clear()
        return signals

    def _route_to_system(self, system_tag, signal_type, event_category, details):
        """
        Placeholder for routing logic to a specific VSM system.
        """
        logger.debug(f"Routing signal to {system_tag}...")
        # In a real implementation, this would interact with the state or message
        # bus of the target system.
        # For example, for S4:
        # if system_tag == "S4":
        #     agent_state = get_agent_state()
        #     agent_state.s4_knowledge.add_learning_from_signal(signal_type, event_category, details)
        #     agent_state.save_s4_knowledge()
        pass

# Singleton instance
algedonic_manager = AlgedonicManager()

def get_algedonic_manager():
    """
    Returns the singleton AlgedonicManager instance.
    """
    return algedonic_manager
