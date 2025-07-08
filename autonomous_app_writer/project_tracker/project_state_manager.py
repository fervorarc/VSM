"""
Manages the state and artifacts for ongoing and completed projects.
"""

import os
import json
import uuid
from autonomous_app_writer import config
from autonomous_app_writer.core.logging_setup import get_logger

logger = get_logger(__name__)

class ProjectStateManager:
    """
    Handles the persistence and retrieval of state for a single project.
    """
    def __init__(self, project_id=None, user_request=""):
        if project_id:
            self.project_id = project_id
        else:
            self.project_id = str(uuid.uuid4())
        
        self.project_dir = os.path.join(config.PROJECTS_DIR, self.project_id)
        self.state_file_path = os.path.join(self.project_dir, "project_state.json")
        
        os.makedirs(self.project_dir, exist_ok=True)
        
        self.state = self._load_state()
        if not self.state:
            self.state = self._initialize_state(user_request)
            self.save_state()

        logger.info(f"ProjectStateManager initialized for project: {self.project_id}")

    def _initialize_state(self, user_request):
        """Initializes a new project state."""
        return {
            "project_id": self.project_id,
            "user_request": user_request,
            "status": "INITIALIZED",
            "iterations_count": 0,
            "structured_requirements": None,
            "architecture_design": None,
            "ui_ux_design": None,
            "code_artifacts": {},
            "test_results": [],
            "audit_findings": [],
            "project_plan": None,
        }

    def _load_state(self):
        """Loads the project state from its JSON file."""
        try:
            with open(self.state_file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def save_state(self):
        """Saves the current project state to its JSON file."""
        with open(self.state_file_path, 'w') as f:
            json.dump(self.state, f, indent=4)
        logger.debug(f"Project state saved for project: {self.project_id}")

    def update_state(self, key, value):
        """Updates a specific key in the project state and saves it."""
        self.state[key] = value
        self.save_state()

    def get_state(self):
        """Returns the entire current project state."""
        return self.state

    def add_code_artifact(self, artifact_name, artifact_content):
        """Saves a code artifact to the project directory."""
        artifact_path = os.path.join(self.project_dir, artifact_name)
        os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
        with open(artifact_path, 'w') as f:
            f.write(artifact_content)
        
        self.state['code_artifacts'][artifact_name] = {"path": artifact_path}
        self.save_state()
        logger.info(f"Saved code artifact '{artifact_name}' for project {self.project_id}")

    def get_project_report(self):
        """Generates a final report for the project."""
        # This is a simple version of the report.
        return {
            "project_id": self.project_id,
            "final_status": self.state.get("status"),
            "summary": "Project development concluded.",
            "artifacts_generated": list(self.state.get('code_artifacts', {}).keys()),
            "test_summary": self.state.get("test_results", [])[-1] if self.state.get("test_results") else "No tests run."
        }
