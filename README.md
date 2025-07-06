# AI-Powered Meal Planner & Grocery List (Backend)

This document provides an overview of the backend services for an AI-powered meal planning and grocery list application. The backend is built using FastAPI and PostgreSQL.

## 1. Introduction

The backend is designed to streamline weekly dinner planning for a family. It uses conversational AI to generate and modify meal plans based on historical eating patterns, family preferences, and practical considerations like time and cost. The application features flexible recipe data storage using PostgreSQL's JSONB, a history-driven meal selection algorithm, and a barcode-centric grocery list.

## 2. Goals & Objectives

*   Generate a dynamic list of 7 dinner meals tailored to family preferences.
*   Enable conversational modification of the meal list via AI.
*   Compile a comprehensive grocery list from planned meals and manual stock reminders.
*   Manage recipes flexibly using PostgreSQL with JSONB.
*   Provide robust export options for meal and grocery lists.
*   Ensure all key configurations are dynamically set at runtime.
*   Provide comprehensive logging for backend operations.

## 3. Scope

This project covers the backend services only, including the FastAPI application, PostgreSQL database, and AI integration. The Nuxt.js frontend, user authentication (beyond a simple API key), and monetization are out of scope.

## 4. Key Features

### Meal Planning & Generation
*   Generates a 7-dinner list without specific dates.
*   Uses an AI-driven workflow with a backend scoring system (`S_recency`, `S_popularity`) to rank meal suggestions.
*   The AI selects 7 meals, ensuring at least one from each category (meat, chicken, fish, vegetarian).
*   Allows conversational modification of the list based on various constraints (time, cost, preferences, dietary restrictions).

### Recipe Management
*   Supports pre-populated and user-added recipes.
*   Uses a PostgreSQL table with a `JSONB` column for flexible recipe details (ingredients, instructions), which can be initially null.

### Grocery List Management
*   Manual, barcode-centric stock reminder system.
*   Aggregates ingredients from the 7-day meal plan into a single grocery list.

### Data Export
*   Exports meal and grocery lists to PDF and clipboard.

## 5. Technical Stack

*   **Backend Framework:** FastAPI (Python)
*   **Database:** PostgreSQL (with JSONB)
*   **Configuration:** Pydantic-Settings
*   **AI Integration:** Pydantic-AI
*   **AI Models:** Gemini / OpenRouter / Ollama
*   **PDF Generation:** TBD (e.g., WeasyPrint, ReportLab)

## 6. Data Models

### `recipes`
*   `id`, `name`, `category`, `active_prep_time_minutes`, `passive_cook_time_minutes`, `cost_level`, `frequency_factor`, `servings_description`, `image_url`, `notes_and_tags`, `recipe_details` (JSONB).

### `meal_history`
*   `id`, `date_eaten`, `meal_name`, `notes`.

### `grocery_items`
*   `id`, `barcode`, `description`, `threshold_amount`, `notes`.

## 7. API Endpoints (Conceptual)

*   `/meals/generate`: Generate a 7-meal list.
*   `/meals/modify`: Modify the current list via conversational prompt.
*   `/recipes`: CRUD operations for recipes.
*   `/history`: Manage meal history.
*   `/grocery-list`: Generate the grocery list.
*   `/grocery-items`: CRUD operations for grocery items.
*   `/export/...`: Export meal and grocery lists.

## 8. System & Non-Functional Requirements

*   **Configuration:** Key constants managed via `Pydantic-Settings`.
*   **Logging:** Comprehensive logging with `Loguru`.
*   **Security:** API endpoints protected by a pre-shared API key.
*   **Performance:** AI responses should be reasonably fast (< 10 seconds).
*   **Maintainability:** Clean, modular, and well-tested code.

## 9. License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.