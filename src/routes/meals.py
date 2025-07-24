from fastapi import APIRouter, HTTPException

from models.meals import Meal, SideDish, MealHistory
from db.repositories.meal import MealRepository
from db.repositories.side_dish import SideDishRepository
from db.repositories.meal_history import MealHistoryRepository
from lib import logger

meal_router = APIRouter(prefix="/meals", tags=["meals"])

# Initialize repositories
meal_repo = MealRepository()
side_dish_repo = SideDishRepository()
meal_history_repo = MealHistoryRepository()


@meal_router.get("/", response_model=list[Meal])
async def get_meals():
    """Get all meals from the database."""
    meals = meal_repo.get_all_meals()
    if meals is None:
        raise HTTPException(
            status_code=500, detail="Failed to fetch meals from the database"
        )
    return meals


@meal_router.get("/side_dishes", response_model=list[SideDish])
async def get_side_dishes():
    """Get all side dishes from the database."""
    side_dishes = side_dish_repo.get_all_side_dishes()
    if side_dishes is None:
        raise HTTPException(
            status_code=500, detail="Failed to fetch side dishes from the database"
        )
    return side_dishes


@meal_router.get("/meal_history", response_model=MealHistory)
async def get_meal_history():
    """Get the complete meal history from the database.

    Returns:
        MealHistory: A MealHistory object containing the meal history items.
        Returns an empty list if no history is found.
    """
    try:
        meal_history = meal_history_repo.get_all_meal_history()
        return meal_history
    except Exception as e:
        logger.error(f"Error fetching meal history: {e}")
        # Return empty meal history on error to maintain consistent response format
        return MealHistory(history=[])


@meal_router.get("/{meal_id}", response_model=Meal)
async def get_meal(meal_id: int):
    """Get a specific meal by ID from the database."""
    meal = meal_repo.get_meal_by_id(meal_id)
    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@meal_router.get("/plan")
def get_plan():
    from lib.ai import get_plan

    # from lib.prompts import system_prompt
    # from fastapi.responses import PlainTextResponse

    # meal_history = get_meal_history()
    # all_foods = get_meals()
    # side_dishes = get_side_dishes()
    # return PlainTextResponse(system_prompt(meal_history, all_foods, side_dishes))
    plan = get_plan()
    return plan


@meal_router.get("/temp/")
def get_temp():
    from fastapi.responses import JSONResponse
    from models.meals import Meal

    return JSONResponse(Meal.model_json_schema())
