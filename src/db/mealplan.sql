CREATE TABLE temp_meal_plan (
    id SERIAL PRIMARY KEY,
    planned_date DATE NOT NULL,
    meal_id INTEGER NOT NULL REFERENCES meals(id),
    side_dish_id INTEGER REFERENCES side_dishes(id),
    is_executed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Add expiration column
    expires_at TIMESTAMP GENERATED ALWAYS AS (created_at + INTERVAL '8 days') STORED
);

-- Create index for efficient cleanup
CREATE INDEX idx_temp_meal_plan_expires ON temp_meal_plan(expires_at);

-- View that automatically filters expired plans
CREATE VIEW current_meal_plan_view AS
SELECT 
    tmp.id,
    tmp.planned_date,
    m.name AS meal,
    sd.name AS side_dish,
    tmp.is_executed
FROM 
    temp_meal_plan tmp
JOIN 
    meals m ON tmp.meal_id = m.id
LEFT JOIN 
    side_dishes sd ON tmp.side_dish_id = sd.id
WHERE 
    tmp.expires_at > CURRENT_TIMESTAMP;

-- Automatic cleanup procedure
CREATE OR REPLACE FUNCTION clean_expired_meal_plans()
RETURNS VOID AS $$
BEGIN
    DELETE FROM temp_meal_plan 
    WHERE expires_at <= CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;