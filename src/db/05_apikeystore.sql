
-- Drop in reverse order of dependencies
DROP VIEW IF EXISTS api_security.provider_keys_view;
DROP FUNCTION IF EXISTS api_security.select_and_log_key_usage() CASCADE;
-- Schema will be dropped with CASCADE to handle all contained objects
DROP SCHEMA IF EXISTS api_security CASCADE;

CREATE SCHEMA api_security;
CREATE TABLE api_security.provider_keys (
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(50) NOT NULL,
    encrypted_key BYTEA NOT NULL,
    key_rotation TIMESTAMPTZ NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_used TIMESTAMPTZ,
    usage_count INT DEFAULT 0,
    metadata JSONB
);

-- 1. Create a function that updates last_used and returns the data
CREATE FUNCTION api_security.select_and_log_key_usage()
RETURNS SETOF api_security.provider_keys AS $$
BEGIN
    UPDATE api_security.provider_keys
    SET last_used = NOW(),
        usage_count = usage_count + 1
    WHERE id IN (SELECT id FROM api_security.provider_keys WHERE is_active = TRUE);
    
    RETURN QUERY SELECT * FROM api_security.provider_keys WHERE is_active = TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 2. Create a view that uses this function
CREATE VIEW api_security.provider_keys_view AS
SELECT * FROM api_security.select_and_log_key_usage();

-- 4. Create role if it doesn't exist and grant necessary permissions
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'api_key_access') THEN
        CREATE ROLE api_key_access NOLOGIN;
    END IF;
    
    -- Grant usage on schema
    GRANT USAGE ON SCHEMA api_security TO api_key_access;
    
    -- Grant access to the view instead of the table
    GRANT SELECT ON api_security.provider_keys_view TO api_key_access;
    
    -- Make sure the table owner has all necessary permissions
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA api_security TO api_key_access;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA api_security TO api_key_access;
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA api_security TO api_key_access;
END
$$;