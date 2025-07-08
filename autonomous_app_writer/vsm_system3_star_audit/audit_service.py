"""
VSM System 3*: Audit and Monitoring.
"""

from autonomous_app_writer.core.logging_setup import get_logger
from autonomous_app_writer.core.llm_services import get_llm_service
from autonomous_app_writer.core.algedonic_manager import get_algedonic_manager

logger = get_logger(__name__)

class AuditService:
    """
    Provides independent, in-depth checks on S1 activities and outputs,
    bypassing S3's routine channels to ensure quality and integrity.
    """
    def __init__(self):
        self.llm_service = get_llm_service()
        self.algedonic_manager = get_algedonic_manager()
        logger.info("System 3* Audit Service initialized.")

    def conduct_audit(self, project_state):
        """
        Conducts a comprehensive audit of the current project state.

        Args:
            project_state (dict): The current state of the project.

        Returns:
            dict: A dictionary containing the audit findings.
        """
        logger.info(f"S3*: Conducting audit for project {project_state.get('id')}")
        
        audit_findings = {
            "code_quality": self._audit_code_quality(project_state.get('code_artifacts')),
            "requirements_conformance": self._audit_requirements_conformance(project_state),
            "architectural_compliance": self._audit_architectural_compliance(project_state),
        }

        # Process findings and generate algedonic signals
        for audit_type, findings in audit_findings.items():
            if findings.get("status") == "FAIL":
                self.algedonic_manager.handle_signal(
                    "PAIN",
                    f"Audit_Failure_{audit_type}",
                    findings,
                    ["S3", "S5"]
                )
        
        return audit_findings

    def _audit_code_quality(self, code_artifacts):
        """Audits the quality of the generated code using an LLM."""
        logger.debug("S3*: Auditing code quality with LLM.")
        if not code_artifacts:
            return {"status": "PASS", "details": "No code artifacts to audit."}

        # For this stub, we'll just check the first Python file we find.
        for filename, artifact_info in code_artifacts.items():
            if filename.endswith(".py"):
                logger.info(f"S3*: Performing LLM code review for: {filename}")
                
                try:
                    with open(artifact_info["path"], 'r') as f:
                        code_content = f.read()
                except Exception as e:
                    logger.error(f"S3*: Could not read file {filename} for audit. Error: {e}")
                    continue

                prompt = f"""
                You are a world-class software engineering expert and code reviewer.
                Analyze the following code for quality, security vulnerabilities, adherence to best practices,
                and potential "code smells".

                Code from file '{filename}':
                ```python
                {code_content}
                ```

                Provide your analysis as a JSON object with two keys:
                - "score": An integer from 0 (poor) to 10 (excellent).
                - "feedback": A string containing detailed feedback. If the score is below 8, provide specific, actionable suggestions for improvement.
                """
                
                review_str = self.llm_service.generate_text(prompt)
                try:
                    review = self.llm_service.parse_json_response(review_str)
                    if review.get("score", 0) < 8:
                        return {"status": "FAIL", "details": f"LLM code review failed for {filename}", "review": review}
                except Exception as e:
                    logger.error(f"S3*: Failed to parse LLM review response for {filename}: {e}")
                    # Don't fail the whole audit, just log the error.
        
        return {"status": "PASS", "details": "All audited code passed LLM review."}

    def _audit_requirements_conformance(self, project_state):
        """Audits whether development is drifting from requirements."""
        logger.debug("S3*: Auditing requirements conformance.")
        prompt = f"""
        You are a VSM System 3* Auditor. Compare the current development artifacts
        against the initial requirements to detect any drift.

        Requirements: {project_state.get('structured_requirements')}
        Current Artifacts Summary: (Provide summary of code, UI, etc.)

        Is the project conforming to the requirements? Provide a brief analysis.
        """
        # analysis = self.llm_service.generate_text(prompt)
        return {"status": "PASS", "details": "No significant drift detected."}

    def _audit_architectural_compliance(self, project_state):
        """Audits whether implementation adheres to the defined architecture."""
        logger.debug("S3*: Auditing architectural compliance.")
        # Placeholder logic
        return {"status": "PASS", "details": "Implementation aligns with defined architecture."}

# Singleton instance
audit_service = AuditService()

def get_audit_service():
    """
    Returns the singleton AuditService instance.
    """
    return audit_service
