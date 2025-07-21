from langchain_core.prompts import ChatPromptTemplate

EMAIL_DRAFT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an AI assistant that drafts professional business emails.
Based on the provided content, write a polite and clear follow-up email.
Ensure the email is well-structured and professional.
"""),
    ("human", "Draft an email based on this content:\n{email_request_content}")
])
