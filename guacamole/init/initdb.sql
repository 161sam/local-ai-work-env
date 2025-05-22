
--
-- Basic Guacamole Database Schema
-- This is a fallback schema if automatic generation fails
--

CREATE TABLE IF NOT EXISTS guacamole_user (
    user_id serial NOT NULL,
    username varchar(128) NOT NULL,
    password_hash bytea NOT NULL,
    password_salt bytea,
    password_date date,
    disabled boolean NOT NULL DEFAULT FALSE,
    expired boolean NOT NULL DEFAULT FALSE,
    access_window_start time,
    access_window_end time,
    valid_from date,
    valid_until date,
    timezone varchar(64),
    full_name varchar(256),
    email_address varchar(256),
    organization varchar(256),
    organizational_role varchar(256),
    PRIMARY KEY (user_id),
    UNIQUE (username)
);

-- Insert default admin user (guacadmin/guacadmin)
INSERT INTO guacamole_user (username, password_hash) VALUES
('guacadmin', decode('ca458a7d494e3be824624a5bbcab46b4d8e1c7e2', 'hex'))
ON CONFLICT (username) DO NOTHING;

-- Other required tables would be here...
-- This is a minimal setup to get started
