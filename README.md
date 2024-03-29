# Microservice

> Installation Requests Service



## About

This project uses [Nameko](http://feathersjs.com). A microservices framework for Python that lets service developers concentrate on application logic and encourages testability.


## Getting Started

1. Ensure that you have a ready python environment 
```
> python --version
Python 3.7.8
```
2. Configure the Pipenv environment https://www.jetbrains.com/help/pycharm/pipenv.html
3. Install dependencies
..

## Local Development with Docker

### 1. Prerequisites
Make sure that you have installed the following tools on your local machine
1. [Docker](https://docs.docker.com/install/#supported-platforms),
2. [docker-compose](https://docs.docker.com/compose/install/). (you should have version 1.29 or higher)
>  Installing [Docker Desktop](https://www.docker.com/products/docker-desktop) (for Mac & Windows) is the easiest way to get your environment ready


### 2. Run a local Rabbit
```
docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```

Check if rabbit is running
```
docker ps
```
also you can do by going to the browser and accessing http://localhost:15672 using credentials guest:guest if you can login to RabbitMQ dashboard it means you have it running locally for development

### 3. Set up the Postgres Database
```
docker run -d --name some-postgres -e POSTGRES_DB=installation_requests_DB -e POSTGRES_PASSWORD=password -e POSTGRES_USER=postgres -p 5433:5432 postgres

# Note: Exposing Postgres on different port for convenience
```
    
You can visualize the database using [pgAdmin tool](https://www.pgadmin.org/). 
Create new server with the following **Connection** informations
```
Host: 127.0.0.1
port: 5433
database: installation_requests_DB
username: postgres
password: password
```

### 4. Run Nameko Service
execute
```bash
alembic upgrade head
```
Once your run the above command, the tables will be generated/updated in the database

Run the nameko service
```bash
nameko run --config config.yml installation_requests.service
```
when you see the following message, it means the service is up and running
```
starting services: installation_requests
```

> :warning: **be careful to config.yml**: uncomment the second bloc, the env variables are added to make the service configurable !


## Test the service
- Insert new installation request in the database with id=1
- Get the installation by Id ==> http://localhost:8000/installation-requests/1
- ...

----------------------------

## Folder Structure

The project structure is like the following
```
  alembic/
    versions/
    env.py    
  installation_requests
    exceptions.py
    models.py
    schemas.py
    service.py  
  tests/
  config.yml
  Pipefile    
```

## Writing tests

### General 
It is a good practice to write tests before you write implementation code.
E.g. you write a test 'should create installation request', that test fails and then write the code for creating installation-request which makes the test succeed

Another way of doing this would be with another developer pair-programming, one developer writes tests, other developer writes the **simplest** solution to make the test pass
Note that you emphasize on making it the simplest solution, so the one writing the test must improve and write better tests

### Testing with pyTest
You find the unit/integration tests inside the `tests` folder.
You can run all the tests by running the following command

```bash
pipenv run coverage run --source=installation_requests -m pytest -v --junit-xml=reports/report.xml  tests && pipenv run coverage xml`
```
...


### Different attributes
#### * Pre-commit
the [pre-commit](https://pre-commit.com/) package manager is already installed (check the `Pipfile`) and configured(check `.pre-commit-config.yml`). to run the hooks `black, pydocstyle, pylint, mypy and commit-message format` and check all the files run 
```bash
pre-commit run --all-files
```

#### * Configurability

#### * Security

#### * Observability
                Sentry��