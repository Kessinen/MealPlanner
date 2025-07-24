# TODO

## High Priority

- [ ] Update meal history to use IDs instead of names for meal and side dish references
  - Modify `add_meal_history` endpoint to accept and use meal_id and side_dish_id
  - Update validation to check for existence using IDs instead of names
  - Update database schema and queries to use foreign key relationships
  - Consider adding database constraints for data integrity

## API Improvements

- [ ] Implement a standard message model for successful operations
  - Create a `MessageResponse` model in `models/responses.py`
  - Include operation status, message, and relevant data in responses
  - Update documentation to reflect the new response format
  - Affected endpoints to update:
    - `POST /meals/meal_history` - Currently returns the created item, should return success message with the item
    - `GET /meals/plan` - Returns raw plan data, should wrap in standard response
    - `GET /meals/temp/` - Returns raw schema, should wrap in standard response
    - `GET /logs/` - Returns raw logs, should wrap in standard response with metadata
    - `GET /logs/{level}` - Returns raw logs, should wrap in standard response with metadata
    - All other CRUD operations in the API
  - Error handling standardization:
    - All endpoints should follow the same error response format
    - Include error codes and user-friendly messages
    - Add proper error logging
