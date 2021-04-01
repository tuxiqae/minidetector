# MiniDetector API

## Description:

A `REST API` which allows users to fetch the entities `minidetector` mapped.

## Endpoints

Since our API was built using`FastAPI`, developers can use their browsers to access the `/` endpoint which contains a
testing environment for the API endpoints. You could also access the `/redoc` endpoint in order to get the `ReDoc`
documentation interface

- `GET /all`
    - Returns a list of all `MAC`, `IP` address pairs
- `GET /routers`
  - Returns a list of `MAC` addresses which appears more than 3 times in the database
- `GET /lastseen`
  - Returns a list of all (`timestamp`, `MAC`, `IP`) trios, ordered by recency