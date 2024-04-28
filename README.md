# Database Design Document

## Purpose
The purpose of this database is to store and manage real estate property listings scraped from the Inmuebles24 website for various states in Mexico. 

## Scope
The scope of this database encompasses the collection of property data including price, location, size, amenities, and descriptions. It aims to provide a comprehensive repository of real estate listings for analysis and reference.

## Entities
1. **inm24**: Represents individual real estate properties.
2. **states**: Stores information about different states including median price, mode price, and total properties recorded.

## Relationships
- The `inm24` table is related to the `states` table through the `property_state` attribute, establishing a connection between property listings and their respective states.

## Optimizations
1. **Indexes**: Indexes are created on `property_state` and `price` columns of the `inm24` table for efficient querying.
2. **Views**: Views are created to present different perspectives of the data:
   - `inm24_no_description`: Excludes the `property_description` column.
   - `inm24_no_large_text`: Excludes large text columns (`property_description`).
   - `all_info`: Joins `inm24` and `states` tables to provide comprehensive property information along with state-level statistics.

## Limitations
1. **Data Completeness**: The completeness of data depends on the availability of listings on the Inmuebles24 website.
2. **Data Accuracy**: Accuracy of scraped data may vary and could be influenced by factors such as data entry errors or outdated listings.

The goal of this design document is to provide clarity and transparency regarding the structure, purpose, and limitations of the database, facilitating understanding and collaboration among stakeholders.


## Future of this prject
The project is developed for creating a full data warehouse with lots of information about the real state market in Mexico, using both historical data and current data, using batch storaging to keep it updated.

## Design
![Database_relation](relations.jpg)