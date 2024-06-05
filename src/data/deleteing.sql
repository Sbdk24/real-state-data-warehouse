DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_property_id' AND conrelid = 'links'::regclass
    ) THEN
        ALTER TABLE links DROP CONSTRAINT fk_property_id;
    END IF;

    ALTER TABLE links
    ADD CONSTRAINT fk_property_id FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL;
END $$;

-- DO $$
-- BEGIN
--     IF EXISTS (
--         SELECT 1 FROM pg_constraint
--         WHERE conname = 'fk_property_id' AND conrelid = 'images'::regclass
--     ) THEN
--         ALTER TABLE images DROP CONSTRAINT fk_property_id;
--     END IF;

--     ALTER TABLE images
--     ADD CONSTRAINT fk_property_id FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL;
-- END $$;



-- DO $$
-- BEGIN
--     IF EXISTS (
--         SELECT 1 FROM pg_constraint
--         WHERE conname = 'fk_property_id' AND conrelid = 'descriptions'::regclass
--     ) THEN
--         ALTER TABLE descriptions DROP CONSTRAINT fk_property_id;
--     END IF;

--     ALTER TABLE descriptions
--     ADD CONSTRAINT fk_property_id FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL;
-- END $$;