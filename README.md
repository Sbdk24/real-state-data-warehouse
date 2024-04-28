# Python Dependencies and Postgres set-up 

### Python:
You'll need to install some libraries for **web scraping and parsing HTML text**:
   *  `pip install beautifulsoup4`
   *  `pip install lxml`
   *  `pip install requests`
   *  `pip install python-dotenv`

### PostgreSQL:
- Mac users: The easiest way to start working with postgreSQL on Mac is to install [Postgres.app]().
  
- Windows/Linux: We're going to use the version provided by [PostgreSQL official website](https://www.postgresql.org/download/). Download
  the lastest stable version.

In both cases, by installing postgres you'll also download a termimnal to manipulate database server. If you perfer to use you own one,
add the activate command to your PATH or just copy and paste the activation link in your terminal.

> [!IMPORTANT]
> Be aware of ports managaging. If you've already downloaded Postgres, it's likely that you have still 5432 port opened
> so you're not be able to start the server, so that, you'll need to troubleshoot its configuration or choose a different port.

# Design and description:

## Purpose
Store and managing real estate property listings scraped from the Inmuebles24 website for various states in Mexico. 

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
![Database_relation](relations.jpg)# real-state-data-warehouse
