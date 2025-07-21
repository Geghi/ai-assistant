import logging
from typing import Dict, Any
from models.agent_state import AgentState
from core.tools import TOOL_MAP

def execute_tool_node(state: AgentState) -> Dict[str, Any]:
    """
    Executes the tool calls identified by the router.
    """
    logging.info(f"Entering execute_tool_node")
    tool_calls = state.tool_calls
    
    if not tool_calls:
        return {"general_response": "No tool calls found to execute."}

    tool_results = []
    for tool_call in tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        
        if tool_name in TOOL_MAP:
            try:
                tool_function = TOOL_MAP[tool_name]
                result = tool_function(**tool_args)
                tool_results.append(f"Tool '{tool_name}' executed successfully: {result.get('message', str(result))}")
            except Exception as e:
                logging.error(f"Error executing tool '{tool_name}': {e}", exc_info=True)
                tool_results.append(f"Error executing tool '{tool_name}': {str(e)}")
        else:
            tool_results.append(f"Unknown tool: {tool_name}")
            
    return {
        "general_response": "\n".join(tool_results)
    }
