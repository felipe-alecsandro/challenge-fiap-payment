# challenge

This is a Django REST Framework project that runs in Docker.

## Burgerstore operation

A functional backend service for customers and store staff can create and manage orders 

## Prerequisites

Before running the project, make sure you have the following installed on your machine:

- Docker (so you can run the project)
- Postgres (so you can manage local database)

## Getting Started

To build and run the project locally, follow these steps:

1. Run docker in your local enviroment

2. In your terminal, run the following command:
    ~sudo docker-compose up -d --build

3. Enter the web image and run create superuser
    sudo docker exec -it web /bin/bash
    python manage.py createsuperuser


