# Python Dependencies and Postgres set-up 
  ### Python:
  You'll need to install some libraries for **web scraping and parsing HTML text**:
  ```
  pip install beautifulsoup4
  pip install lxml
  pip install requests
  pip install python-dotenv
  ```

  For postgres manipulation with python we'll use 
  ```
  pip install psycopg2
  ```
  It's working on localhost, nevertheless if you're using 
  some other server, go ahead and change my server configuartion on `median_mode.py`.
  
  ### PostgreSQL:
  - Mac users: The easiest way to start working with postgreSQL is to install [Postgres.app](https://postgresapp.com/).
    
  - Windows/Linux: We're going to use the version provided by [PostgreSQL official website](https://www.postgresql.org/download/).
    Download the lastest stable version.
  
  In both cases, by installing postgres you'll also get a termimnal to manipulate database server. 
  If you perfer to use your own one, add the activate command to your PATH or just copy and paste the activation link in your terminal.
  
  > [!IMPORTANT]
  > Be aware of ports managaging. If you've already downloaded Postgres, it's likely that you still have port 5432 opened
  > and you won't be able to run the server, so that, you'll need to troubleshoot its configuration or set a different port.

# Design and description:

  ## General purpose:
   Storing and managing real estate property listings scraped from various websites to get current data about real-state market for all states in Mexico. 

  
  ### Data Retrieval
   
   **Functions:**
   
  - `main():` Iterates over states and pages within each state to extract data.
  - `get_status(url):` It makes HTTP requests to a URL until a successful response is obtained or a retry limit is reached.
  - `extract_data(properties, state):` Extracts relevant information from each real estate property on a specific page.
  - `parse_property_info(amenities):` Parses the features of a property to extract information such as square meters, rooms, bathrooms, and parking spaces.
  
> [!NOTE]
> It's better to use headers to simulate a web browser request and states which contains information about states and their
> corresponding URLs on inmuebles24.com.

## DB Design:

### Entities
   1. **inm24**: Represents individual real estate properties.
   2. **states**: Stores information about different states including median price, mode price, and total properties recorded.

### Relationships
  - The `inm24` table is related to the `states` table through the `property_state` attribute, establishing a connection between property listings and their respective states.

### Optimizations
  1. **Indexes**: Indexes are created on `property_state` and `price` columns of the `inm24` table for efficient querying.
  2. **Views**: Views are created to present different perspectives of the data:
     - `inm24_no_description`: Excludes the `property_description` column.
     - `inm24_no_large_text`: Excludes large text columns (`property_description`).
     - `all_info`: Joins `inm24` and `states` tables to provide comprehensive property information along with state-level statistics.

### Limitations
  1. **Data Completeness**: The completeness of data depends on the availability of listings on the Inmuebles24 website.
  2. **Data Accuracy**: Accuracy of scraped data may vary and could be influenced by factors such as data entry errors or outdated listings.

