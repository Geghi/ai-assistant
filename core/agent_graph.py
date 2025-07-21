import logging
from langgraph.graph import StateGraph, END
from models.agent_state import AgentState
from core.llm_provider import get_llm_model
from core.nodes import (
    router_node,
    email_draft_generator_node,
    general_message_handler_node,
    execute_tool_node, # Import the new execute_tool_node
)

logging.basicConfig(level=logging.INFO)

# Create a LangGraph StateGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("router", router_node)
workflow.add_node("email_draft_generator", email_draft_generator_node)
workflow.add_node("general_message_handler", general_message_handler_node)
workflow.add_node("execute_tool", execute_tool_node) # Add the execute_tool_node

# Set the entry point
workflow.set_entry_point("router")

# Define conditional edges based on the 'next_node' from the router
workflow.add_conditional_edges(
    "router",
    lambda state: state.next_node,
    {
        "email_draft_generator": "email_draft_generator",
        "general_message_handler": "general_message_handler",
        "execute_tool": "execute_tool", # Route to execute_tool if a tool call is identified
    },
)

# Add edges from the terminal nodes to END
workflow.add_edge("email_draft_generator", END)
workflow.add_edge("general_message_handler", END)
workflow.add_edge("execute_tool", END) # Tool execution is a terminal node for now

# Compile the graph
app = workflow.compile()

async def process_telegram_update(message_text: str, message_type: str = "text"):
    """
    Processes a single Telegram update by running it through the LangGraph.
    """
    llm = get_llm_model()
    inputs = {
        "input_message": message_text,
        "message_type": message_type,
        "llm": llm,
    }
    
    logging.info(f"Received new input message: {inputs['input_message'], inputs['message_type']}")
    final_state = app.invoke(inputs)
    
    response_to_user = None
    if final_state.get("email_draft"):
        response_to_user = f"Here is your email draft:\n\n{final_state['email_draft']}"
    elif final_state.get("general_response"):
        response_to_user = final_state["general_response"]
    else:
        response_to_user = "An unexpected error occurred or tool executed." # More specific message needed here
        
    return response_to_user

__all__ = ["app", "process_telegram_update", "AgentState"]
