# Mini Detector

## Description

The `minidetector` is an app which sniffs network traffic in order to map the network.

`minidetector` is built upon 2 sub-projects:

- [`sniffer`](./minidetector) - Sniffs the packets and inserts MAC, IP address pairs into the database.
- [`api`](./api) - Allows users to fetch the mapped data from the DB using a safe and sound interface.

--------

## Installation

**Dependencies:**

- `Docker`
- `Docker Compose`

In order to run `minidetector` execute the following command:
`$ docker-compose up`

This command will run both services, and the DB container as configured in the `docker-compose.yml` file.

```
user in minidetector on  master is 📦 v0.1.0 via 🐍 v3.8.0
 ❯ docker-compose up
Starting minidetector_postgres_1 ... done
Starting minidetector_sniffer_1  ... done
Starting minidetector_api_1      ... done
Attaching to minidetector_postgres_1, minidetector_sniffer_1, minidetector_api_1
postgres_1  | 
postgres_1  | PostgreSQL Database directory appears to contain a database; Skipping initialization
postgres_1  | 
postgres_1  | 2021-03-31 15:57:52.787 UTC [1] LOG:  starting PostgreSQL 13.2 (Debian 13.2-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
postgres_1  | 2021-03-31 15:57:52.787 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
postgres_1  | 2021-03-31 15:57:52.787 UTC [1] LOG:  listening on IPv6 address "::", port 5432
postgres_1  | 2021-03-31 15:57:52.793 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
postgres_1  | 2021-03-31 15:57:52.800 UTC [25] LOG:  database system was shut down at 2021-03-31 15:57:50 UTC
postgres_1  | 2021-03-31 15:57:52.823 UTC [1] LOG:  database system is ready to accept connections
api_1       | INFO:     Started server process [1]
api_1       | INFO:     Waiting for application startup.
api_1       | INFO:     Application startup complete.
api_1       | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
sniffer_1   | INFO:root:Queue size: 1
sniffer_1   | INFO:root:Queue size: 1
sniffer_1   | INFO:root:Queue size: 12
sniffer_1   | INFO:root:Queue size: 1
```