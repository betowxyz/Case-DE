# Case - DE

## Question 1
To replace the `produce_consume` role (id=3) with the `manage` role (id=4) for the `user` Taylor (id=2), we can run:
```sql
UPDATE
    user_role_rela
SET
    role_id = 4
WHERE
    user_id = 2
    AND role_id = 3;
```

This single statement replaces the user's role, allowing Taylor to modify products while no longer having permission to change the company's inventory.

## Question 2
### 1. Creation of the tables
[SQL code available here](./tables.sql).

### 2. ETL Code
The [ETL](./src/) process executes the following steps:

1. Authenticate against the API.
2. Retrieve all genres and upsert them into the `genre` table.
3. For each genre:
   - Retrieve the associated movies.
   - Populate the `movie_genre` relationship table.
   - Collect unique movie IDs.
4. Retrieve the details of each unique movie and upsert them into the `movie` table.
5. Retrieve the ratings for each movie and upsert them into the `review` table.

The pipeline is idempotent by design. All writes use PostgreSQL UPSERTs (`INSERT ... ON CONFLICT`), allowing safe retries, reruns, or full refreshes without creating duplicate records.

#### Some decisions
- Retry mechanism for API requests.
- Idempotent writes using PostgreSQL UPSERTs (`INSERT ... ON CONFLICT`).
- Basic logging.
- Batch writes to PostgreSQL for improved performance.
- I would add tests and data quality checks but would need more time / info about the data.
