import os
import json
import re
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel
from core.config import settings
from services.openai_service import OpenAIService
from services.google_service import GoogleService
from prompts.router_prompt import ROUTER_PROMPT
from prompts.email_draft_prompt import EMAIL_DRAFT_PROMPT
import logging

logging.basicConfig(level=logging.INFO)

LLM_PROVIDER = settings.LLM_PROVIDER

llm = None
if LLM_PROVIDER == "openai":
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
elif LLM_PROVIDER == "google":
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                                google_api_key=settings.GOOGLE_API_KEY
)
else:
    raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}. Choose 'openai' or 'google'.")

class AgentState(BaseModel):
    input_message: str = ""
    message_type: str = "text"
    email_request_content: Optional[str] = None
    email_draft: Optional[str] = None
    general_response: Optional[str] = None
    next_node: Optional[str] = None


def parse_llm_response(response_content: str) -> dict:
    try:
        # Remove markdown-style ```json ... ``` block if present
        cleaned = re.sub(r"```json\n(.*?)\n```", r"\1", response_content.strip(), flags=re.DOTALL)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"general_response": response_content}
    except Exception as e:
        logging.error(f"Failed to parse LLM response: {e}", exc_info=True)
        return {"general_response": "Error parsing LLM response."}


def router_node(state: AgentState) -> Dict[str, Any]:
    """
    Routes the incoming message to the appropriate node based on intent.
    Determines if the user wants to create an email or handle a general message.
    """
    logging.info(f"Entering router_node with state: {state}")
    user_message = state.input_message
    
    # Use the LLM to process the router prompt
    chain = ROUTER_PROMPT | llm
    response = chain.invoke({"user_message": user_message})
    
    parsed_response = parse_llm_response(response.content)

    next_node = parsed_response.get("next_node", "general_message_handler")
    email_request_content = parsed_response.get("email_request_content")
    general_response = parsed_response.get("general_response")

    if next_node == "email_draft_generator" and not email_request_content:
        next_node = "general_message_handler"
        general_response = "It looks like you want to draft an email, but I didn't get the content. Please try again."

    if not general_response and next_node == "general_message_handler":
        general_response = f"I've received your message: '{user_message}'. How can I help you today?"

    return {
        "next_node": next_node,
        "email_request_content": email_request_content,
        "general_response": general_response
    }

def email_draft_generator_node(state: AgentState) -> Dict[str, Any]:
    """
    Generates an email draft using the LLM.
    """
    logging.info(f"Entering email_draft_generator_node with state: {state.json()}")
    # Accessing state attributes using dot notation as AgentState is a Pydantic BaseModel
    email_request_content = state.email_request_content
    
    if not email_request_content:
        return {"email_draft": "Error: No content provided for email draft."}
        
    chain = EMAIL_DRAFT_PROMPT | llm
    
    try:
        response = chain.invoke({"email_request_content": email_request_content})
        email_draft = response.content
        return {"email_draft": email_draft}
    except Exception as e:
        logging.error(f"Error generating email draft: {e}", exc_info=True)
        return {"email_draft": f"Error generating email draft: {e}"}

def general_message_handler_node(state: AgentState) -> Dict[str, Any]:
    """
    Handles general messages that are not email creation requests.
    """
    logging.info(f"Entering general_message_handler_node with state: {state}")
    # The router_node already populates general_response.
    # This node could potentially do more, like logging or simple text processing.
    # For now, it just passes through the general response.
    return {"general_response": state.general_response}

# Create a LangGraph StateGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("router", router_node)
workflow.add_node("email_draft_generator", email_draft_generator_node)
workflow.add_node("general_message_handler", general_message_handler_node)

# Set the entry point
workflow.set_entry_point("router")

# Define conditional edges based on the 'next_node' from the router
workflow.add_conditional_edges(
    "router",
    lambda state: state.next_node,
    {
        "email_draft_generator": "email_draft_generator",
        "general_message_handler": "general_message_handler",
    }
)

# Add edges from the terminal nodes to END
workflow.add_edge("email_draft_generator", END)
workflow.add_edge("general_message_handler", END)

# Compile the graph
# In a real application, you would configure checkpointing here if needed.
# For example: memory = Memory(config={"session_id": "my_session"})
# app = workflow.compile(checkpointer=memory)
app = workflow.compile()

# This part would be called from your FastAPI application when a Telegram update is received.
async def process_telegram_update(message_text: str, message_type: str = "text"):
    """
    Processes a single Telegram update by running it through the LangGraph.
    """
    inputs = {
        "input_message": message_text,
        "message_type": message_type # This would come from the Telegram update object
    }
    
    logging.info(f"Received new input message: {inputs}")
    # Execute the graph
    # The invoke method returns the final state of the graph.
    final_state = app.invoke(inputs)
    
    logging.info(f"Final state: {final_state}")
    # Determine the response to send back to Telegram
    response_to_user = None
    if final_state.get("email_draft"):
        response_to_user = f"Here is your email draft:\n\n{final_state['email_draft']}"
    elif final_state.get("general_response"):
        response_to_user = final_state["general_response"]
    else:
        response_to_user = "An unexpected error occurred."
        
    return response_to_user

__all__ = ["app", "process_telegram_update", "AgentState"]
