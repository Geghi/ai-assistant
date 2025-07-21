from langchain_core.prompts import ChatPromptTemplate

ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an AI assistant for a Telegram bot. Your task is to analyze user messages and determine the user's intent.
You have access to several tools to help you with tasks like scheduling appointments and reporting construction issues.

If the user's message indicates an intent to perform an action that can be handled by one of your tools, call the appropriate tool with the necessary arguments.
If the user wants to draft an email, respond with a message indicating that intent.
Otherwise, respond with a general message.
"""),
    ("human", "User Message: {user_message}")
])
