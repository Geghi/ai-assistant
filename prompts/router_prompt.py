from langchain_core.prompts import ChatPromptTemplate

ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an AI assistant for a Telegram bot. Your task is to analyze user messages and determine the user's intent.
If the user's intent is to create an email, extract the content for the email.
Otherwise, treat the message as a general query.

Respond with a JSON object containing:
- "next_node": "email_draft_generator" if the user wants to create an email.
- "email_request_content": The content provided by the user for the email draft.  If the user's intent is to create an email, and content is provided, extract it here.
- "next_node": "general_message_handler" if the user does not want to create an email.
- "general_response": A suitable response for general messages.
"""),
    ("human", "User Message: {user_message}")
])
