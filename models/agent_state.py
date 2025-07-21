from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    llm: Optional[Any] = Field(None, exclude=True)
    input_message: str = ""
    message_type: str = "text"
    email_request_content: Optional[str] = None
    email_draft: Optional[str] = None
    appointment_request_content: Optional[str] = None # This will be deprecated with tool use
    construction_issue_content: Optional[str] = None # This will be deprecated with tool use
    tool_calls: Optional[List[Dict[str, Any]]] = None # To store tool calls from LLM
    general_response: Optional[str] = None
    next_node: Optional[str] = None
