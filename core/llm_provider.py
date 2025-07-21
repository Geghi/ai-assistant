from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings

def get_llm_model():
    """
    Returns the appropriate LLM model based on the provider specified in the settings.
    """
    llm_provider = settings.LLM_PROVIDER

    if llm_provider == "openai":
        return ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
    elif llm_provider == "google":
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            google_api_key=settings.GOOGLE_API_KEY,
        )
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {llm_provider}. Choose 'openai' or 'google'.")
