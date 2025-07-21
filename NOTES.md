# AI Assistant Task Expansion Notes

This document outlines the plan to extend the AI assistant's capabilities based on the `project_context.md`. The focus is on tasks that can be handled via Telegram messages.

## 1. New Nodes to be Created

New nodes will be created in the `core/nodes/` directory to handle specific tasks. Each node will encapsulate the logic for its designated function.

### a. `appointment_scheduler_node.py`

*   **Purpose:** Manages all aspects of appointment scheduling, including creating new appointments, rescheduling, and confirming them.
*   **Key Functionality:**
    *   Parse user requests for scheduling or rescheduling.
    *   Interact with a calendar service (e.g., Google Calendar) to check for availability.
    *   Propose alternative meeting times.
    *   Handle communication with the other party to confirm the new time.
    *   Update the calendar with the confirmed appointment.

### b. `construction_issue_node.py`

*   **Purpose:** Handles incoming reports of construction site issues.
*   **Key Functionality:**
    *   Classify the urgency of the issue (urgent vs. routine).
    *   If urgent, immediately notify the user (Charan) and the relevant site manager.
    *   If routine, schedule the issue for the daily briefing.
    *   Draft an automated response to acknowledge receipt of the issue.
    *   Track the resolution status of the issue.

## 2. Updates to the Router

The `router_node.py` and `router_prompt.py` will be updated to include the new nodes as possible destinations.

### a. `prompts/router_prompt.py`

*   The `ROUTER_PROMPT` will be updated to include the new tasks (appointment scheduling and construction issue reporting) as intents that the LLM can identify.
*   The prompt will instruct the LLM to extract relevant information for each task (e.g., for an appointment, the name of the other party, the reason for the meeting, and any scheduling constraints).

### b. `core/nodes/router_node.py`

*   The `router_node` function will be updated to handle the new `next_node` values.
*   It will route to `appointment_scheduler` or `construction_issue_handler` based on the LLM's response.
*   It will pass the extracted information to the corresponding node.

## 3. Agent Graph Integration

The new nodes will be added to the agent graph in `core/agent_graph.py`. The graph will be updated to include conditional edges from the `router_node` to the new nodes.

This plan provides a clear path to extending the AI assistant's functionality. Once you approve this plan, I can begin implementation. Please let me know if you have any feedback or would like to proceed.
