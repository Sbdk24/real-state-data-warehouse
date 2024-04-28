-- Update the 'neighborhood' column in the 'inm24' table, setting NULL where it's 'NULL'
UPDATE inm24 
SET neighborhood = NULL
WHERE neighborhood = 'NULL';

-- Update the 'property_description' column in the 'inm24' table, setting NULL where it's 'NULL'
UPDATE inm24 
SET property_description = NULL
WHERE property_description = 'NULL';

-- Calculate the average price from the 'price' column in the 'inm24' table
SELECT AVG(price) AS average_price FROM inm24;

-- Alter the 'price' column in the 'inm24' table, allowing NULL values
ALTER TABLE inm24
ALTER COLUMN price DROP NOT NULL;

-- Count records where price is 0 or 1 in the 'inm24' table
SELECT COUNT(*) FROM inm24 WHERE price = 0::money OR price = 1::money;

-- Find the maximum price for each property_state in the 'inm24' table
SELECT MAX(price::numeric), property_state FROM inm24
GROUP BY property_state;

-- Drop the 'no_desc' view
DROP VIEW no_desc;

-- Alter the data type of 'property_state' column to VARCHAR(25) in the 'inm24' table
ALTER TABLE inm24
ALTER COLUMN property_state TYPE VARCHAR(25);

-- Count occurrences of each property_state in the 'inm24' table
SELECT COUNT(*), property_state AS number_of_states
FROM inm24
GROUP BY property_state;

-- Calculate the median price for 'ciudad de mexico' from the 'inm24' table
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY price::numeric) AS mediana
FROM inm24 WHERE property_state = 'ciudad de mexico';

-- Find the mode price and its frequency in the 'inm24' table
SELECT DISTINCT price AS mode_price, COUNT(*) OVER (PARTITION BY price::numeric) AS frequency
FROM inm24
ORDER BY frequency DESC
LIMIT 1;

-- Provide execution plan for the query selecting specific columns from 'inm24' where 'property_state' is 'ciudad de mexico'
EXPLAIN 
SELECT price, maintenance, property_state, neighborhood, property_address 
FROM inm24 
WHERE property_state = 'ciudad de mexico';

-- Similar to previous, find the mode price and its frequency using a subquery
SELECT DISTINCT price AS mode_price, COUNT(*) 
OVER (PARTITION BY price::numeric) AS frequency
FROM (
    SELECT property_state, price 
    FROM inm24 
    ) AS states
ORDER BY frequency DESC LIMIT 1; 

-- Insert distinct 'property_state' values into 'states' table from 'inm24' table
INSERT INTO states (country_state)
SELECT DISTINCT property_state from inm24;
