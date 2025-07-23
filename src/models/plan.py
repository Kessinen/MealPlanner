from pydantic import BaseModel, Field

from .meals import MealType


class MealPlanItem(BaseModel):
    id: int = Field(description="Iteration number.")
    meal_name: str = Field(description="Name of the meal.")
    meal_type: list[MealType] = Field(description="Type of meal.")
    side_dish: str | None = Field(description="Side dish of the meal.")
    notes: str | None = Field(description="Notes about the meal.")


class MealPlan(BaseModel):
    plan: list[MealPlanItem] = Field(description="Meal plan for the week.")
