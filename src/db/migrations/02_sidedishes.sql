-- Drop in reverse order of dependencies
DROP TRIGGER IF EXISTS update_side_dish_timestamp ON side_dishes;
DROP FUNCTION IF EXISTS update_timestamp() CASCADE;
DROP TABLE IF EXISTS side_dishes CASCADE;

-- Create side_dishes table
CREATE TABLE side_dishes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add automatic timestamp update function
CREATE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for side_dishes
CREATE TRIGGER update_side_dish_timestamp
BEFORE UPDATE ON side_dishes
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();