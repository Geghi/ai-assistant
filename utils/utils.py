import re
import json
import logging
from pydantic import BaseModel, ValidationError
from typing import Type, TypeVar

T = TypeVar('T', bound=BaseModel)

def parse_llm_response(response_content: str) -> dict:
    try:
        # Remove markdown-style ```json ... ``` block if present
        cleaned = re.sub(r"```json\n(.*?)\n```", r"\1", response_content.strip(), flags=re.DOTALL)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logging.warning(f"LLM response is not valid JSON: {response_content}")
        return {"general_response": response_content}
    except Exception as e:
        logging.error(f"Failed to parse LLM response: {e}", exc_info=True)
        return {"general_response": "Error parsing LLM response."}

def parse_llm_response_with_pydantic(response_content: str, model: Type[T]) -> T:
    try:
        # Remove markdown-style ```json ... ``` block if present
        cleaned = re.sub(r"```json\n(.*?)\n```", r"\1", response_content.strip(), flags=re.DOTALL)
        return model.model_validate_json(cleaned)
    except ValidationError as e:
        logging.error(f"Pydantic validation error for model {model.__name__}: {e}", exc_info=True)
        raise ValueError(f"Invalid data for {model.__name__}: {e}")
    except json.JSONDecodeError:
        logging.error(f"LLM response is not valid JSON for Pydantic model {model.__name__}: {response_content}")
        raise ValueError(f"Invalid JSON response for {model.__name__}")
    except Exception as e:
        logging.error(f"Failed to parse LLM response with Pydantic model {model.__name__}: {e}", exc_info=True)
        raise RuntimeError(f"Error processing LLM response for {model.__name__}: {e}")
