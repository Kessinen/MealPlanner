from fastapi import APIRouter
import json

from models.meals import Meal, SideDish, MealHistoryItem, MealHistory

meal_router = APIRouter(prefix="/meals")


@meal_router.get("/")
def get_meals():
    with open("data.json", "r") as f:
        data = json.load(f)
        all_foods = data["all_foods"]
        return [Meal(**food) for food in all_foods]


@meal_router.get("/side_dishes")
def get_side_dishes():
    with open("data.json", "r") as f:
        data = json.load(f)
        side_dishes = data["side_dishes"]
        return [SideDish(**side_dish) for side_dish in side_dishes]


@meal_router.get("/meal_history")
def get_meal_history():
    with open("data.json", "r") as f:
        data = json.load(f)
        meal_history = data["history"]
        meal_history = MealHistory(
            history=[
                MealHistoryItem(**meal_history_item)
                for meal_history_item in meal_history
            ]
        )
        return meal_history


@meal_router.get("/plan")
def get_plan():
    from lib.prompts import system_prompt
    from fastapi.responses import PlainTextResponse

    meal_history = get_meal_history()
    all_foods = get_meals()
    side_dishes = get_side_dishes()
    return PlainTextResponse(system_prompt(meal_history, all_foods, side_dishes))
