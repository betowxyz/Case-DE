# Case - DE

## Question 1
Since we want to unassign the role `produce_consume`(id=3) and assign the role `manage`(4) for the user Taylor(id=2), we just need to run:
```sql
UPDATE
    user_role_rela
SET
    role_id = 4
WHERE
    user_id = 2
    AND role_id = 3;
```

In this way with a single SQL statement, it will be able to modify products but not to change company's inventory.

## Question 2
In src we have everything that was asked:
- [Creation of the tables](./tables.sql)
- [ETL code](./src/)

Decisions:
- Retry mechanism for API requests.
- Idempotent writes using PostgreSQL UPSERTs (`INSERT ... ON CONFLICT`).
- Basic logging.
- Batch writes to PostgreSQL for improved performance.
- I would add tests and data quality checks but would need more time / info about the data.
