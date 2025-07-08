"""
VSM System 3: Operational Management & Internal Regulation.
Manages the "here and now" of the entire app development lifecycle.
"""

from typing import TypedDict, List
from autonomous_app_writer.core.logging_setup import get_logger
from autonomous_app_writer.core.langgraph_orchestrator import LangGraphOrchestrator
from autonomous_app_writer.core.agent_state import get_agent_state
from autonomous_app_writer.project_tracker.project_state_manager import ProjectStateManager

logger = get_logger(__name__)

# Define the state for the S3 project management workflow
class S3WorkflowState(TypedDict):
    project_manager: ProjectStateManager
    task_list: List[dict]
    completed_tasks: List[dict]
    current_task_result: dict
    final_result: dict

class ProjectLifecycleManager:
    """
    Orchestrates the entire app development lifecycle for a single project
    using a LangGraph workflow.
    """
    def __init__(self, user_request):
        self.agent_state = get_agent_state()
        self.project_manager = ProjectStateManager(user_request=user_request)
        self.workflow = self._build_workflow()
        logger.info(f"S3 ProjectLifecycleManager initialized for project {self.project_manager.project_id}")

    def _build_workflow(self):
        """Builds the LangGraph workflow for managing the project."""
        orchestrator = LangGraphOrchestrator(S3WorkflowState)

        # Define nodes
        orchestrator.add_node("start_project", self.start_project)
        orchestrator.add_node("plan_and_design", self.plan_and_design)
        orchestrator.add_node("decompose_into_tasks", self.decompose_into_tasks)
        orchestrator.add_node("execute_task", self.execute_task)
        orchestrator.add_node("evaluate_task_result", self.evaluate_task_result)
        orchestrator.add_node("finalize_project", self.finalize_project)

        # Define edges
        orchestrator.set_entry_point("start_project")
        orchestrator.add_edge("start_project", "plan_and_design")
        orchestrator.add_edge("plan_and_design", "decompose_into_tasks")
        orchestrator.add_edge("decompose_into_tasks", "execute_task")
        orchestrator.add_edge("execute_task", "evaluate_task_result")

        # Conditional edge for the main development loop
        orchestrator.add_conditional_edge(
            "evaluate_task_result",
            self.decide_next_step,
            {
                "continue": "execute_task",
                "rework": "execute_task", # Or a new "rework_task" node
                "audit": "conduct_audit",
                "end": "finalize_project"
            }
        )
        
        # Audit loop
        orchestrator.add_node("conduct_audit", self.conduct_audit)
        orchestrator.add_edge("conduct_audit", "execute_task")

        return orchestrator.compile()

    # --- Workflow Node Functions ---

    def start_project(self, state):
        logger.info("S3 Node: start_project")
        # This is the entry point, state is already initialized.
        return {"project_manager": self.project_manager, "task_list": [], "completed_tasks": []}

    def plan_and_design(self, state):
        logger.info("S3 Node: plan_and_design")
        pm = state["project_manager"]

        # 1. Elicit Requirements
        req_task = {"user_prompt": pm.get_state()["user_request"]}
        req_result = self.agent_state.get_s1_agent("RequirementsAgent").execute_task(req_task, pm.get_state())
        if req_result["status"] == "FAILURE":
            raise Exception("Requirements elicitation failed.")
        pm.update_state("structured_requirements", req_result["artifact"])

        # 2. Design Architecture
        arch_result = self.agent_state.get_s1_agent("ArchitectureAgent").execute_task({}, pm.get_state())
        if arch_result["status"] == "FAILURE":
            raise Exception("Architecture design failed.")
        pm.update_state("architecture_design", arch_result["artifact"])

        # 3. Design UI/UX
        ui_ux_result = self.agent_state.get_s1_agent("UiUxAgent").execute_task({}, pm.get_state())
        if ui_ux_result["status"] == "FAILURE":
            raise Exception("UI/UX design failed.")
        pm.update_state("ui_ux_design", ui_ux_result["artifact"])
        
        logger.info("S3: Planning and design phase completed.")
        return state

    def decompose_into_tasks(self, state):
        logger.info("S3 Node: decompose_into_tasks")
        pm = state["project_manager"]
        project_state = pm.get_state()

        prompt = f"""
        You are a System 3 project manager. Based on the project requirements and architecture,
        decompose the work into a detailed list of tasks for the S1 operational agents.
        
        Requirements: {project_state.get('structured_requirements')}
        Architecture: {project_state.get('architecture_design')}

        Provide a JSON list of tasks. Each task should be a dictionary with 'description' and 'agent' keys.
        The 'agent' key must be one of the available agent names (e.g., 'FrontendCoderAgent', 'BackendCoderAgent', 'DatabaseAgent', 'UnitTesterAgent').
        Ensure tasks are ordered logically (e.g., database schema before API, API before UI).
        """
        
        llm_service = self.agent_state.get_s1_agent("RequirementsAgent").llm_service # Reuse an LLM service
        response_str = llm_service.generate_text(prompt)
        
        try:
            tasks = llm_service.parse_json_response(response_str)
            logger.info(f"Decomposed project into {len(tasks)} tasks.")
            return {**state, "task_list": tasks}
        except Exception as e:
            logger.error(f"Failed to decompose tasks: {e}")
            raise

    def execute_task(self, state):
        logger.info("S3 Node: execute_task")
        pm = state["project_manager"]
        task_list = state["task_list"]
        
        if not task_list:
            # This should not be reached if the logic is correct, but as a safeguard:
            return {**state, "current_task_result": {"status": "NO_TASKS"}}

        current_task = task_list.pop(0)
        agent_name = current_task.get("agent")
        s1_agent = self.agent_state.get_s1_agent(agent_name)
        
        if s1_agent:
            logger.info(f"S3: Assigning task '{current_task.get('description')}' to {agent_name}")
            result = s1_agent.execute_task(current_task, pm.get_state())
            return {**state, "current_task_result": result, "completed_tasks": state["completed_tasks"] + [current_task]}
        else:
            logger.error(f"S3: Could not find agent '{agent_name}' for task. Skipping.")
            return {**state, "current_task_result": {"status": "AGENT_NOT_FOUND"}}

    def evaluate_task_result(self, state):
        logger.info("S3 Node: evaluate_task_result")
        pm = state["project_manager"]
        result = state["current_task_result"]
        
        if result.get("status") == "SUCCESS":
            artifact = result.get("artifact")
            if artifact and isinstance(artifact, dict) and "filename" in artifact and "content" in artifact:
                pm.add_code_artifact(artifact["filename"], artifact["content"])
                # After a successful coding task, we can add a testing task.
                if "CoderAgent" in result.get("agent_name", ""):
                     test_task = {"description": f"Write unit tests for {artifact['filename']}", "agent": "UnitTesterAgent", "code_artifact": artifact}
                     state["task_list"].insert(0, test_task)

        return state

    def decide_next_step(self, state):
        logger.info("S3 Node: decide_next_step")
        if state["current_task_result"].get("status") != "SUCCESS":
            logger.error("Task failed. Adding rework task to the queue.")
            # Add a rework task to the front of the queue
            rework_task = state["completed_tasks"][-1] # The failed task
            rework_task["rework_count"] = rework_task.get("rework_count", 0) + 1
            if rework_task["rework_count"] > 2: # Limit reworks
                logger.error("Maximum rework attempts reached. Ending workflow.")
                return "end"
            state["task_list"].insert(0, rework_task)
            return "rework"
        
        # Trigger an audit every 3 completed tasks (for demonstration)
        if len(state["completed_tasks"]) % 3 == 0 and len(state["completed_tasks"]) > 0:
            return "audit"

        if state["task_list"]:
            return "continue"
        else:
            return "end"

    def conduct_audit(self, state):
        logger.info("S3 Node: conduct_audit")
        pm = state["project_manager"]
        audit_service = self.agent_state.get_s1_agent("AuditService") # Assuming it's registered like an S1
        if not audit_service:
            # In a real system, AuditService might be accessed differently
            from autonomous_app_writer.vsm_system3_star_audit.audit_service import get_audit_service
            audit_service = get_audit_service()

        audit_findings = audit_service.conduct_audit(pm.get_state())
        pm.update_state("audit_findings", pm.get_state().get("audit_findings", []) + [audit_findings])
        return state

    def finalize_project(self, state):
        logger.info("S3 Node: finalize_project")
        pm = state["project_manager"]
        
        # 1. Generate Documentation
        doc_task = {"description": "Generate the project README file."}
        doc_result = self.agent_state.get_s1_agent("DocumentationAgent").execute_task(doc_task, pm.get_state())
        if doc_result["status"] == "SUCCESS":
            artifact = doc_result["artifact"]
            pm.add_code_artifact(artifact["filename"], artifact["content"])
        else:
            logger.warning("Documentation generation failed.")

        # 2. Generate Deployment Scripts (e.g., Dockerfile)
        deploy_task = {"description": "Generate Dockerfile for the application.", "type": "generate_dockerfile"}
        deploy_result = self.agent_state.get_s1_agent("DeploymentAgent").execute_task(deploy_task, pm.get_state())
        if deploy_result["status"] == "SUCCESS":
            artifact = deploy_result["artifact"]
            pm.add_code_artifact(artifact["filename"], artifact["content"])
        else:
            logger.warning("Dockerfile generation failed.")
            
        pm.update_state("status", "COMPLETED")
        logger.info(f"Project {pm.project_id} finalized successfully.")
        
        return {**state, "final_result": pm.get_project_report()}

    def check_if_more_tasks(self, state):
        return "continue" if state["task_list"] else "end"

    def run(self):
        """Executes the project lifecycle workflow."""
        logger.info(f"S3: Starting development lifecycle for project {self.project_manager.project_id}")
        initial_state = {
            "project_manager": self.project_manager,
            "task_list": [],
            "completed_tasks": [],
            "final_result": None
        }
        final_state = self.workflow.invoke(initial_state)
        logger.info(f"S3: Project lifecycle finished with state: {final_state}")
        return final_state
