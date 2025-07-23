from fastapi import HTTPException
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.providers.mistral import MistralProvider

from dotenv import load_dotenv
import os

from models.plan import MealPlan
from .prompts import system_prompt
from routes.meals import get_meal_history, get_meals, get_side_dishes

load_dotenv()


def _get_prompt():
    meal_history = get_meal_history()
    all_foods = get_meals()
    side_dishes = get_side_dishes()
    return system_prompt(meal_history, all_foods, side_dishes, days=7)


def get_ollama_model(
    name: str = "hf.co/mradermacher/Qwen3-53B-A3B-TOTAL-RECALL-MASTER-CODER-v1.4-GGUF:latest",
):
    model = OpenAIModel(
        model_name=name,
        provider=OpenAIProvider(base_url="http://localhost:11434/v1"),
    )
    return model


def get_openrouter_model(
    name: str = "qwen/qwen3-235b-a22b-07-25:free",
    api_key: str = os.getenv("OPENROUTER_API_KEY", ""),
):
    if not api_key:
        raise HTTPException(status_code=400, detail="OpenRouter API key not found")
    model = OpenAIModel(
        model_name=name,
        provider=OpenRouterProvider(api_key=api_key),
    )
    return model


def get_mistral_model(
    name: str = "moonshotai/kimi-k2:free",
    api_key: str = os.getenv("MISTRAL_API_KEY", ""),
):
    if not api_key:
        raise HTTPException(status_code=400, detail="Mistral API key not found")
    model = MistralModel(
        model_name=name,
        provider=MistralProvider(api_key=api_key),
    )
    return model


def get_plan():
    from rich import print

    print("Getting plan...")
    model_name = "mistral-small-latest"
    agent = Agent(
        model=get_mistral_model(model_name),
        system_prompt=_get_prompt(),
        output_type=MealPlan,
    )
    try:
        result = agent.run_sync("")
    except Exception as e:
        match e.status_code:
            case 404:
                raise HTTPException(
                    status_code=404, detail=f"Model {model_name} not found"
                )
            case 401:
                raise HTTPException(
                    status_code=401,
                    detail=f"Trying to use {model_name}, but got Unauthorized",
                )
            case 403:
                raise HTTPException(
                    status_code=403,
                    detail=f"Trying to use {model_name}, but got Forbidden",
                )
            case 429:
                raise HTTPException(
                    status_code=429,
                    detail=f"Trying to use {model_name}, but got Too many requests",
                )
            case 500:
                raise HTTPException(
                    status_code=500,
                    detail=f"Trying to use {model_name}, but got Internal server error",
                )
            case _:
                raise HTTPException(
                    status_code=500,
                    detail=f"Trying to use {model_name}, but got Unknown error",
                )
    print(result)
    return result.output
