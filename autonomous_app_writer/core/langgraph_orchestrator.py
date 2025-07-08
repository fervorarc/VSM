"""
Utilities and wrappers for defining and running LangGraph workflows.
"""

# This file will depend on the 'langgraph' library.
# Ensure it is installed: pip install langgraph

from langgraph.graph import StateGraph, END
from autonomous_app_writer.core.logging_setup import get_logger

logger = get_logger(__name__)

class LangGraphOrchestrator:
    """
    A helper class to build and execute LangGraph workflows.
    """
    def __init__(self, state_class):
        """
        Initializes the orchestrator with a specific state definition.

        Args:
            state_class (TypedDict): A TypedDict class defining the graph's state.
        """
        self.workflow = StateGraph(state_class)
        self.state_class = state_class
        logger.info(f"LangGraph orchestrator initialized with state: {state_class.__name__}")

    def add_node(self, node_name, node_function):
        """
        Adds a node to the workflow graph.

        Args:
            node_name (str): The name of the node.
            node_function (callable): The function to execute for this node.
        """
        self.workflow.add_node(node_name, node_function)
        logger.debug(f"Added node '{node_name}' to graph.")

    def add_edge(self, start_node, end_node):
        """
        Adds a directed edge between two nodes.

        Args:
            start_node (str): The name of the starting node.
            end_node (str): The name of the ending node.
        """
        self.workflow.add_edge(start_node, end_node)
        logger.debug(f"Added edge from '{start_node}' to '{end_node}'.")

    def add_conditional_edge(self, start_node, condition_function, conditional_mapping):
        """
        Adds a conditional edge based on the output of a condition function.

        Args:
            start_node (str): The name of the starting node.
            condition_function (callable): A function that returns a string key.
            conditional_mapping (dict): A dictionary mapping keys to node names.
        """
        self.workflow.add_conditional_edges(
            start_node,
            condition_function,
            conditional_mapping
        )
        logger.debug(f"Added conditional edge from '{start_node}'.")

    def set_entry_point(self, node_name):
        """
        Sets the entry point for the workflow.

        Args:
            node_name (str): The name of the entry point node.
        """
        self.workflow.set_entry_point(node_name)
        logger.info(f"Set graph entry point to '{node_name}'.")

    def compile(self):
        """
        Compiles the workflow into a runnable graph.

        Returns:
            A compiled LangGraph app.
        """
        logger.info("Compiling LangGraph workflow.")
        return self.workflow.compile()

# Example of a state definition (would be defined in the specific workflow file)
# from typing import TypedDict, List
#
# class ExampleWorkflowState(TypedDict):
#     input_request: str
#     processed_data: dict
#     final_result: str
#     error_message: str
