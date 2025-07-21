import logging
from typing import Dict, Any
from models.agent_state import AgentState

def general_message_handler_node(state: AgentState) -> Dict[str, Any]:
    """
    Handles general messages that are not email creation requests.
    """
    logging.info(f"Entering general_message_handler_node")
    # The router_node already populates general_response.
    # This node could potentially do more, like logging or simple text processing.
    # For now, it just passes through the general response.
    return {"general_response": state.general_response}
