-- Create a table 'inm24' if it doesn't exist, defining its schema
CREATE TABLE IF NOT EXISTS inm24 (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    price MONEY,
    maintenance MONEY,
    currency VARCHAR(3) NOT NULL,
    property_state VARCHAR(25),
    neighborhood VARCHAR(200),
    property_address VARCHAR(200),
    meters INT,
    rooms SMALLINT,
    bathrooms SMALLINT,
    parking_spaces SMALLINT,
    property_description TEXT
);

-- Create a table 'states' if it doesn't exist, defining its schema
CREATE TABLE IF NOT EXISTS states (
    id SERIAL NOT NULL PRIMARY KEY,
    country_state VARCHAR(21),
    median_price MONEY,
    mode_price MONEY,
    properties_recorded INTEGER 
);

-- Create a view 'inm24_no_description' selecting specific columns from 'inm24' table
CREATE VIEW inm24_no_description AS 
SELECT id, price, maintenance, currency,
property_state, neighborhood, property_address,
meters, rooms, bathrooms, parking_spaces
FROM inm24;

-- Create a view 'inm24_no_large_text' selecting specific columns except 'property_description' from 'inm24' table
CREATE VIEW inm24_no_large_text AS
SELECT id, price, maintenance, currency,
meters, rooms, bathrooms, parking_spaces
FROM inm24;

-- Create a view 'all_info' joining 'inm24' and 'states' tables and selecting specific columns
CREATE VIEW all_info AS
SELECT price, maintenance, currency,
property_state, neighborhood, property_address,
meters, rooms, bathrooms, parking_spaces,
states.median_price, states.mode_price, properties_recorded 
FROM inm24
JOIN states on inm24.property_state = states.country_state;

-- Create an index 'sort_by_state' on 'property_state' column of 'inm24' table
CREATE INDEX sort_by_state ON inm24(property_state);

-- Create an index 'sort_by_price' on 'price' column of 'inm24' table
CREATE INDEX sort_by_price ON inm24(price);
