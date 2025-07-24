-- Seed data for meals table
-- Generated from data.json

-- Clear existing data (if any)
TRUNCATE TABLE meals RESTART IDENTITY CASCADE;

-- Insert meals from all_foods
INSERT INTO meals (name, meal_types, notes, frequency_factor, active_time, passive_time, has_side_dish) VALUES
('Grilliruokaa', '{meat,chicken,fish,vegetable}', 'Summer only.', 1, NULL, NULL, true),
('Hernekeitto', '{meat,vegetable}', 'Emppu does not eat.', 1, NULL, NULL, false),
('Jauhelihakastike', '{meat}', NULL, 1, NULL, NULL, true),
('Lasagnette', '{meat,vegetable}', NULL, 1, NULL, NULL, false),
('Kanasalaatti', '{chicken}', NULL, 1, NULL, NULL, false),
('Maksalaatikko', '{meat}', NULL, 1, NULL, NULL, false),
('Munakastike', '{vegetable}', NULL, 1, NULL, NULL, true),
('Pastasalaatti', '{vegetable}', NULL, 1, NULL, NULL, false),
('McDonalds', '{meat,chicken,fish,vegetable}', 'Fast food', 1, NULL, NULL, false),
('Porsaansuikalekastike', '{meat}', NULL, 1, NULL, NULL, true),
('Makaronimössö', '{meat,vegetable}', NULL, 1, NULL, NULL, false),
('Lohi medaljongit', '{fish}', NULL, 1, NULL, NULL, true);

-- Update the updated_at timestamp to match the current time for all records
UPDATE meals SET updated_at = NOW();