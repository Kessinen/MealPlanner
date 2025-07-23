-- Simplified meal_history table without timestamps
CREATE TABLE meal_history (
    id SERIAL PRIMARY KEY,
    date_eaten DATE NOT NULL,
    meal_id INTEGER NOT NULL REFERENCES meals(id),
    side_dish_id INTEGER REFERENCES side_dishes(id)
);

-- View remains the same
CREATE VIEW meal_history_view AS
SELECT
    mh.id,
    mh.date_eaten,
    m.name AS meal,
    sd.name AS side_dish
FROM
    meal_history mh
JOIN
    meals m ON mh.meal_id = m.id
LEFT JOIN
    side_dishes sd ON mh.side_dish_id = sd.id;