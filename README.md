# Ecom-challenge Project

## Intro

This project aims to develop an API to manage sales/inventory of an e-commerce, which will be consumed by an Angular application.

Developed as a challenge for the position of Fullstack developer at IATECAM company.

## Requirements

I decided to use docker to facilitate the execution of the API. You can get installation details for your operating system through the following link: https://docs.docker.com/get-docker/

Once docker is installed and running on your machine, you will need to upload a container with a PostgreSQL instance to persist the data managed by the API. Use the following command:

```shell
docker run --name PostgreSQL -p 5432:5432 -e POSTGRES_DB={ db_name } -e POSTGRES_PASSWORD={ db_password } -d postgres
```

**PS**: *Don't forget to replace the { dbname } and { db_password } fields, as these will be the database access credentials through the API*

The following libraries were used for development:

- ### Backend

  - fastapi: version 0.103.0

  - uvicorn: version 0.23.2

  - requests: version 2.28.2

  - httpx: version 0.24.1

  - SQLAlchemy: version 2.0.20

  - psycopg2-binary: version 2.9.7

  - passlib: version 1.7.4

  - bcrypt: version 4.0.1

  - #### For tests:

    - pytest: version 7.4.0

  - #### Tools:

    - alembic: version: 1.11.3

## Running

First, download or clone this repository to your preferred directory. 

- ### Backend

  ​	Once you have access to this repository and the **PostgreSQL** container is running, run the following commands in your preferred terminal:

  ```shell
  cd backend
  docker build -t ecomm-api . 
  docker run -p 80:80 -e SQLALCHEMY_DATABASE_URL=postgresql://postgres:{ db_password }@{ postgres_IPAddress }/{ db_name } ecomm-api
  ```

  

  **PS**: *Don't forget to replace the { dbname } and { db_password } fields, which are the same used in the execution of the **PostgreSQL** container. Para obter o { postgre_IPAddress } utilize o seguinte comando:*

  ```shell
  docker ps # To get PostgreSQL container identifier
  docker inspect 74c3 | grep IPAddress
  ```



