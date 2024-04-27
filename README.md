# Champions League Data

## Overview

The Champions League Data project provides a way to visualize the results of European football matches on a map.
It allows users to view the history for a given football team in Champions League, Europa League and Europa Conference League.

## Architecture

The project is structured with four Docker containers managed by a docker-compose file:

1. **Database**: A DynamoDB database using the `amazon/dynamodb-local` image. It contains two tables: `games` and `teams`.
2. **UI for Database Management**: A web interface for managing the DynamoDB database. You can access it through [DynamoDB Admin](https://github.com/aaronshaf/dynamodb-admin)
3. **Data Scraper**: A Python-based scraper that fetches data on teams and games from the UEFA website. It populates the database within a few minutes.
4. **API Service**: An API that provides data to the front-end application.

The front-end is a simple HTML file (`index.html`) with an accompanying JavaScript file (`main.js`) to visualize the data.

## Setup and Usage

### Requirements
- Docker

### Instructions 

1. Start Docker Compose

'''sh
docker-compose up --build -d
'''

This will:
- Initialize the database with the appropriate tables.
- Start the Python scraper to populate the database with data.
- Launch the DynamoDB UI at http://localhost:8001, where you can view and manage the data.
- Start the API service, available at http://localhost:8000.

2. Access the Front-End
Once the Docker containers are running, open `index.html` in your web browser. You can now search for your favorite football team's data and view it on the map.
