# Image Search App - Setup Instructions

## Prerequisites
- Docker and Docker Compose installed
- Google API key and Search Engine ID

## Setup


1. Create a `.env` file in the root directory with the following content:
    ```
    GOOGLE_API_KEY=your_google_api_key
    SEARCH_ENGINE_ID=your_search_engine_id
    ```
2. Build and start the services with Docker Compose:
    ```
    docker-compose up --build
    ```

## Access the Application

1. Once the services are up, navigate to `http://localhost:3000` in your browser.
2. Enter a search query (e.g., "small white dog") and hit Enter to see results.

## Testing

To run the tests:

1. Run the following command:
    ```
    docker-compose run tests
    ```

This will run the unit tests for the server, client, and integration.