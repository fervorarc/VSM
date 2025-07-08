"""
VSM System 5: Policy, Identity, and Ultimate Governance.
This daemon runs in the background to adapt the agent's core policies.
"""

import time
from autonomous_app_writer import config
from autonomous_app_writer.core.logging_setup import get_logger
from autonomous_app_writer.core.agent_state import get_agent_state
from autonomous_app_writer.core.llm_services import get_llm_service
from autonomous_app_writer.core.algedonic_manager import get_algedonic_manager

logger = get_logger(__name__)

class System5PolicyDaemon:
    """
    Defines the agent's core mission, ethical guidelines, and high-level
    development philosophies. Adapts policies based on performance and strategy.
    """
    def __init__(self, adaptation_interval=86400): # Default adaptation interval: 24 hours
        self.agent_state = get_agent_state()
        self.llm_service = get_llm_service()
        self.algedonic_manager = get_algedonic_manager()
        self.adaptation_interval = adaptation_interval
        logger.info("System 5 Policy Daemon initialized.")

    def run(self):
        """
        The main loop for the daemon.
        """
        logger.info("System 5 Daemon starting its run loop.")
        while True:
            if config.ENABLE_S5_DAEMON_ADAPTATION:
                logger.info("S5: Starting policy review and adaptation cycle.")
                try:
                    self.review_and_adapt_policies()
                except Exception as e:
                    logger.error(f"S5: An error occurred during policy adaptation: {e}", exc_info=True)
            else:
                logger.info("S5: Policy adaptation is disabled by feature flag.")
            
            logger.info(f"S5: Policy review complete. Sleeping for {self.adaptation_interval} seconds.")
            time.sleep(self.adaptation_interval)

    def review_and_adapt_policies(self):
        """
        Reviews strategic inputs and performance feedback to adapt policies.
        """
        current_policies = self.agent_state.s5_policies
        s4_knowledge = self.agent_state.s4_knowledge
        
        # In a real system, this would also pull high-level performance summaries
        # from S3, perhaps via the algedonic manager.
        performance_summary = self._get_performance_summary()

        prompt = f"""
        As the ultimate governance system (System 5) of an autonomous agent,
        review the current policies, strategic environmental knowledge, and
        long-term performance summary. Propose adaptations to the policies if necessary.

        Current Policies:
        {current_policies}

        Strategic Knowledge from System 4:
        {s4_knowledge}

        Performance Summary:
        {performance_summary}

        Based on this, should any policies be updated? If so, provide the updated
        policy document as a structured JSON object. If not, respond with the original policies.
        Your response should be only the JSON policy document.
        """

        response_str = self.llm_service.generate_text(prompt, model=config.DEFAULT_MAIN_MODEL)

        try:
            # This assumes the LLM returns a valid JSON string.
            # Robust error handling and parsing would be needed here.
            updated_policies = self.llm_service.parse_json_response(response_str) # Assumes such a method exists
            self.agent_state.s5_policies = updated_policies
            self.agent_state.save_s5_policies()
            logger.info("S5: Successfully reviewed and updated policies.")
        except Exception as e:
            logger.error(f"S5: Failed to parse LLM response or update policies: {e}")

    def _get_performance_summary(self):
        """
        Gathers long-term performance data from the algedonic signal queue.
        """
        signals = self.algedonic_manager.get_signals() # Assumes this method exists
        if not signals:
            return {"summary": "No performance signals recorded recently."}

        pain_signals = [s for s in signals if s['type'] == 'PAIN']
        pleasure_signals = [s for s in signals if s['type'] == 'PLEASURE']

        # Simple summary logic
        failure_categories = [s['category'] for s in pain_signals]
        success_categories = [s['category'] for s in pleasure_signals]

        return {
            "recent_failure_count": len(failure_categories),
            "recent_success_count": len(success_categories),
            "common_failure_points": list(set(failure_categories)),
            "common_success_points": list(set(success_categories)),
        }

if __name__ == '__main__':
    # This allows running the daemon as a standalone script for testing.
    from autonomous_app_writer.core.logging_setup import setup_logging
    setup_logging()
    daemon = System5PolicyDaemon(adaptation_interval=60) # Short interval for testing
    daemon.run()
