-- Table is created to only contains unrepeteated data and non too long strings columns
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL NOT NULL PRIMARY KEY,
    price MONEY,
    maintenance MONEY,
    currency VARCHAR(3),
    location_p VARCHAR(200),
    address_p VARCHAR(200),
    meters INTEGER,
    rooms SMALLINT,
    bathrooms SMALLINT,
    parking_spaces SMALLINT,
    link_id INTEGER,
    description_id INTEGER,
    state_id INTEGER,
    advertiser_id INTEGER
);


-- All states in Mexico and some fundamental insights from the data
CREATE TABLE IF NOT EXISTS states (
    id SERIAL NOT NULL PRIMARY KEY,
    state_name VARCHAR(21),
    median MONEY,
    mode MONEY,
    properties_listed INTEGER
);


-- Real state companies who advertised properties in this project
CREATE TABLE IF NOT EXISTS advertisers (
    id SERIAL NOT NULL PRIMARY KEY,
    adverstiver_name VARCHAR(15),
    median MONEY,
    mode MONEY,
    properties_listed INTEGER,
    domain TEXT
);

-- Links table associated with its property
CREATE TABLE IF NOT EXISTS links (
    id SERIAL NOT NULL PRIMARY KEY,
    property_id INTEGER NOT NULL,
    link TEXT
);

-- Images table associated with its property
CREATE TABLE IF NOT EXISTS images (
    id SERIAL NOT NULL PRIMARY KEY,
    property_id INTEGER NOT NULL,
    image_p BYTEA
);

-- Descriptions table associated with its property
CREATE TABLE IF NOT EXISTS descriptions (
    id SERIAL NOT NULL PRIMARY KEY,
    property_id INTEGER NOT NULL,
    description_p TEXT
);

-- Constraints created to reference one to one tables with the properties one


-- ------------EXPLAIN THIS IN MORE DETAIL -------------------------------

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_property_id' AND conrelid = 'links'::regclass
    ) THEN 
        ALTER TABLE links
        ADD CONSTRAINT fk_property_id FOREIGN KEY (property_id) REFERENCES properties(id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_property_id' AND conrelid = 'images'::regclass
    ) THEN 
        ALTER TABLE images
        ADD CONSTRAINT fk_property_id FOREIGN KEY (property_id) REFERENCES properties(id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_property_id' AND conrelid = 'descriptions'::regclass
    ) THEN 
        ALTER TABLE descriptions
        ADD CONSTRAINT fk_property_id FOREIGN KEY (property_id) REFERENCES properties(id);
    END IF;
END $$;

-- Constraints created to relate all tables (except images due to its nature) with the main one

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_link_id' AND conrelid = 'properties'::regclass
    ) THEN 
        ALTER TABLE properties
        ADD CONSTRAINT fk_link_id FOREIGN KEY (link_id) REFERENCES links(id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_description_id' AND conrelid = 'properties'::regclass
    ) THEN 
        ALTER TABLE properties
        ADD CONSTRAINT fk_description_id FOREIGN KEY (description_id) REFERENCES descriptions(id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_state_id' AND conrelid = 'properties'::regclass
    ) THEN 
        ALTER TABLE properties
        ADD CONSTRAINT fk_state_id FOREIGN KEY (state_id) REFERENCES states(id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_advertiser_id' AND conrelid = 'properties'::regclass
    ) THEN 
        ALTER TABLE properties
        ADD CONSTRAINT fk_advertiser_id FOREIGN KEY (advertiser_id) REFERENCES advertisers(id);
    END IF;
END $$;






-- DO $$
-- BEGIN
--     IF EXISTS (
--         SELECT 1 FROM pg_constraint
--         WHERE conname = 'fk_link_id' AND conrelid = 'properties'::regclass
--     ) THEN
--         ALTER TABLE properties DROP CONSTRAINT fk_link_id;
--     END IF;

--     ALTER TABLE properties
--     ADD CONSTRAINT fk_link_id FOREIGN KEY (link_id) REFERENCES links(id) ON DELETE SET NULL;
-- END $$;


-- DO $$
-- BEGIN
--     IF EXISTS (
--         SELECT 1 FROM pg_constraint
--         WHERE conname = 'fk_description_id' AND conrelid = 'properties'::regclass
--     ) THEN
--         ALTER TABLE properties DROP CONSTRAINT fk_description_id;
--     END IF;

--     ALTER TABLE properties
--     ADD CONSTRAINT fk_description_id FOREIGN KEY (description_id) REFERENCES descriptions(id) ON DELETE SET NULL;
-- END $$;


