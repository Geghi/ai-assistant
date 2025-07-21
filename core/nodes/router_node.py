import logging
from typing import Dict, Any
from models.agent_state import AgentState
from prompts.router_prompt import ROUTER_PROMPT
from core.tools import TOOLS # Import the tools

def router_node(state: AgentState) -> Dict[str, Any]:
    """
    Routes the incoming message to the appropriate node based on intent,
    potentially identifying a tool call.
    """
    logging.info(f"Entering router_node")
    user_message = state.input_message
    llm = state.llm
    
    # Bind tools to the LLM for function calling
    llm_with_tools = llm.bind_tools(TOOLS)
    
    # Use the LLM to process the router prompt and potentially call a tool
    chain = ROUTER_PROMPT | llm_with_tools
    response = chain.invoke({"user_message": user_message})

    tool_calls = response.tool_calls
    
    if tool_calls:
        # If the LLM decided to call a tool, pass the tool calls to the next node
        return {
            "next_node": "execute_tool",
            "tool_calls": tool_calls,
            "general_response": None # Clear general response if a tool is called
        }
    else:
        # If no tool call, it's a general message or email draft request
        general_response = response.content
        
        # Simple keyword-based check for email drafting
        if "draft an email" in user_message.lower() or "write an email" in user_message.lower():
            return {
                "next_node": "email_draft_generator",
                "email_request_content": user_message, # Pass original message for email drafting
                "general_response": None
            }
        else:
            return {
                "next_node": "general_message_handler",
                "general_response": general_response
            }
