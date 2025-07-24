from pydantic import BaseModel, Field
from enum import Enum
from datetime import date


class MealType(Enum):
    MEAT = "meat"
    CHICKEN = "chicken"
    FISH = "fish"
    VEGETABLE = "vegetable"


class Meal(BaseModel):
    name: str = Field(description="Name of the meal.")
    meal_types: list[MealType] = Field(
        examples=[
            [MealType.MEAT],
            [MealType.CHICKEN],
            [MealType.CHICKEN, MealType.VEGETABLE],
            [MealType.FISH, MealType.VEGETABLE],
            [MealType.MEAT, MealType.CHICKEN, MealType.FISH, MealType.VEGETABLE],
        ],
        description="Type of meal. Some meals can be multiple types depending on the ingredients used.",
    )
    notes: str | None = Field(default=None, description="Notes about the meal.")
    frequency_factor: float = Field(
        default=1.0,
        description="Factor to adjust the frequency of the meal.",
    )
    active_time: int | None = Field(
        default=None,
        description="Preparation (active) time in minutes.",
    )
    passive_time: int | None = Field(
        default=None,
        description="Cooking (passive) time in minutes.",
    )
    has_side_dish: bool = Field(
        default=True,
        description="Whether the meal has a side dish.",
    )


class SideDish(BaseModel):
    name: str = Field(
        description="Name of the side dish.", examples=["Peruna", "Riisi", "Pasta"]
    )
    notes: str | None = Field(default=None, description="Notes about the side dish.")


class MealHistoryItem(BaseModel):
    date_eaten: date = Field(..., description="Date when the meal was eaten.")
    meal: str = Field(description="Meal that was eaten.")
    side_dish: str | None = Field(default=None, description="Side dish of the meal.")


class MealHistory(BaseModel):
    history: list[MealHistoryItem] = Field(..., description="History of meals eaten.")
