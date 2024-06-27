# Customer Stats API

## Overview

This project provides an API to fetch daily statistics for customers from a pre-populated SQLite database. It is designed for simplicity and testing purposes.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.

### Setting Up

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/robert011192/rated-network.git
    cd <repository-directory>
    ```

2. **Build and Run the Application**:
    Simply run the following command to build the Docker containers and start the application:
    ```sh
    docker-compose up --build
    ```

3. **Check the Readme**:
    - The database is already created and populated.
    - `generator.py` has been run to set up the necessary data.

### Testing

- There is a `test_main.http` file at the root of the project. This file contains various endpoints that cover edge cases. You can use tools like [HTTPie](https://httpie.io/) or any HTTP client to test these endpoints.

### API Endpoints

#### Get Customer Stats

- **Endpoint**: `/customers/{id}/stats`
- **Method**: `GET`
- **Query Parameters**:
  - `from` (alias: `from_`): Start date in `YYYY-MM-DD` format.

- **Response**: 
  - `200 OK`: Returns a list of daily statistics for the specified customer.
  - `400 Bad Request`: If the date format is invalid.
  - `404 Not Found`: If the customer does not exist or if there are no records found for the given date range.
  - `500 Internal Server Error`: For any other errors.

### Note on Bytewax

Currently, using Bytewax has not been successful. More time is needed to get familiar with the library and adapt to the latest changes in methods, many of which have been replaced or removed.
