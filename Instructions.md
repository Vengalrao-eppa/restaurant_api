This is a demo app for restaurant API.

## Setting up the project.

1) Setup the virtual ENV: python3 -m venv env
2) Activate env: source env/bin/activate 
3) Install the requirements:  pip install -r requirement.txt
4) Run the project: GO to the root of the project and enter command: python manage.py runserver

## Setup PSQL database as backend

1) Install depencies for ubunutu : apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
   For window: Install from officeal webiste exe file
2) Login to PSQL: psql -U <username>
3) Create database: CREATE DATABASE restaurantapi;
4) exit;

## Running with the docker
1) Create build: docker-compose build .
2) Run the build: docker-compose up -d --build
3) Close the container: docker-compose down
4) To create the Database : 
      docker-compose exec db psql -U postgres 
      CREATE DATABASE <databasename>;
      exit;

# For external migratration / command
docker-compose exec web python manage.py migrate