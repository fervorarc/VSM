"""
A simple Gradio-based web UI for the Autonomous App-Writing Agent.
"""

import gradio as gr
from autonomous_app_writer.main import initialize_agent, handle_development_request

# Initialize the agent once when the UI starts
initialize_agent()

def run_agent(user_prompt):
    """
    The function that Gradio will call to run the agent.
    """
    if not user_prompt:
        return "Please provide a description of the application you want to build."
    
    # This will run the full development lifecycle.
    # In a real application, this should be run asynchronously and provide progress updates.
    result = handle_development_request(user_prompt)
    
    # Format the result for display
    final_report = result.get("final_result", {})
    return f"""
    ## Development Complete!

    **Project ID:** {final_report.get('project_id')}
    **Final Status:** {final_report.get('final_status')}

    ### Summary
    {final_report.get('summary')}

    ### Artifacts Generated
    ```
    {chr(10).join(final_report.get('artifacts_generated', []))}
    ```

    ### Final Test Summary
    ```
    {final_report.get('test_summary')}
    ```
    """

# Create the Gradio interface
iface = gr.Interface(
    fn=run_agent,
    inputs=gr.Textbox(lines=5, label="App Description", placeholder="e.g., A simple to-do list app for the web."),
    outputs=gr.Markdown(label="Development Result"),
    title="Autonomous App-Writing Agent",
    description="Enter a description of the application you want to build, and the agent will attempt to create it.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()
