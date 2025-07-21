import logging
from typing import Dict, Any
from models.agent_state import AgentState
from prompts.email_draft_prompt import EMAIL_DRAFT_PROMPT

def email_draft_generator_node(state: AgentState) -> Dict[str, Any]:
    """
    Generates an email draft using the LLM.
    """
    logging.info(f"Entering email_draft_generator_node with state: {state.json()}")
    # Accessing state attributes using dot notation as AgentState is a Pydantic BaseModel
    email_request_content = state.email_request_content
    llm = state.llm
    
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
