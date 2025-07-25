DROP TYPE IF EXISTS meal_type CASCADE;
DROP TABLE IF EXISTS meals CASCADE;
DROP TRIGGER IF EXISTS update_meal_timestamp ON meals CASCADE;
DROP FUNCTION IF EXISTS update_timestamp CASCADE;

-- Create the meal type enum (simple DB-level validation)
CREATE TYPE meal_type AS ENUM ('meat', 'chicken', 'fish', 'vegetable');

-- Core table with just what we need
CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    meal_types meal_type[] NOT NULL,
    notes TEXT,
    frequency_factor FLOAT DEFAULT 1.0,
    active_time INTEGER,
    passive_time INTEGER,
    has_side_dish BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automatic timestamp function (the one useful addition)
CREATE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_meal_timestamp
BEFORE UPDATE ON meals
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

