# Python Flask Example - Hotel Reservation Service

The **Hotel Reservation Service** example is a GraphQL API providing the ability to create and list reservations as well as the ability to list available rooms for a given date range.

Booked reservations are listed via the API. Each reservation request were processed in the order provided as if they were real-time requests. The following rules are observed:

**Context**:

* When a room is reserved, it cannot be reserved by another guest on overlapping dates.
* Whenever there are multiple available rooms for a request, the room with the lower final price is assigned.
* Whenever a request is made for a single room, a double bed room may be assigned (if no single is available?).
* Smokers are not placed in non-smoking rooms.
* Non-smokers are not placed in allowed smoking rooms.
* Final price for reservations are determined by daily price * num of days requested, plus the cleaning fee.

**Usage**

Example usage via [curl](https://curl.se/download.html):

```bash
# List all existing booked reservations
curl http://localhost:$API_PORT/development/api \
    -H 'Content-Type: application/json' \
    -d '{"query": "query { getAllReservations { reservations { room_id checkin_date checkout_date  } } }"}'

# Create a new reservation
# Note: if there is an overlap, you'll see a 
#   'Reservation dates overlap with an existing reservation' error message
# To see the aforementioned error, run this mutation a multiple times
curl http://localhost:$API_PORT/development/api \
    -H 'Content-Type: application/json' \
    -d '{ "query": "mutation { createReservation( input: { room_id: \"91754a14-4885-4200-a052-e4042431ffb8\", checkin_date: \"2023-12-31\", checkout_date: \"2024-01-02\", total_charge: 111 }) { success errors reservation { id room_id checkin_date checkout_date total_charge } } }" }'

# List Available Rooms for a given date range
curl http://localhost:$API_PORT/development/api \
    -H 'Content-Type: application/json' \
    -d '{"query": "query { getAvailableRooms( input: { checkin_date: \"2023-12-31\", checkout_date: \"2024-01-02\" }) { success errors rooms { id num_beds allow_smoking daily_rate cleaning_fee } } }" }'
```

**Table of Contents**:

* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
    - [Install Python Packages](#install-python-packages)
    - [Install Node.js Packages](#install-nodejs-packages)
    - [Create the Database](#create-the-database)
* [Development](#development)
* [Testing](#testing)
* [Troubleshooting](#troubleshooting)
    - [Docker Image](#docker-image)
* [License](#license)

## Prerequisites

To run the service, you will need to install the following tools.

* [Python](https://www.python.org/downloads/)
* [NodeJS](https://nodejs.org/en/) - Used for migrations ([Knex.js](https://knexjs.org/)). 

For migrations, [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/index.html) or [Alembic](https://alembic.sqlalchemy.org/en/latest/) are suitable options, but I prefer using **Knex.js** due to familiarity.

The below are optional:

* [nvm](https://github.com/nvm-sh/nvm) - Used to manage NodeJS versions.
* [Direnv](https://direnv.net/) - Used to manage environment variables.
* [Docker](https://www.docker.com/)  - We can containerize the hotel reservation service:
    - Push the container to [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/)
    - Once in ECR, serve the container as an [AWS Elastic Container service](https://aws.amazon.com/ecs/).
    - We can then use the [Application Load Balancer](https://aws.amazon.com/elasticloadbalancing/application-load-balancer/) to distribute traffic across ECS tasks.

## Getting Started

First, we'll need to set up our environment variables.  You can do this by either:

* Manually exporting the necessary environment variables in your shell.  These are listed in the [`./envrc.example`](./envrc.example) file.

or

* Use optionally use **Direnv**.

```bash
cp .envrc.example .envrc
direnv allow
```

For exporting environment variables, [Python Dotenv](https://pypi.org/project/python-dotenv/) is an option as well.  However, **Direnv** is preferred as it isn't dependent on Python therefore can be used in other use-cases.

### Install Python Packages

Execute the following in your terminal:

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip 
pip install -r requirements.txt
```

### Install Node.js Packages

Execute the following within your terminal:

```bash
nvm use             # To eliminate any issues, install/use the version listed in .nvmrc. 
npm i               # install the packages needed for project 
```

### Create the database

Finally, let's create and seed the databases and our Reservations and Rooms tables:

```bash
# Create the databases and seed them
NODE_ENV=development | ./create_db.sh && npm run refresh
NODE_ENV=test | ./create_db.sh && npm run refresh
```

## Development

To run the service locally:

```bash
docker-compose up -d  # runs the database in the background
python src/main.py
```

To verify the service is working:

```bash
curl http://localhost:$API_PORT/$ENV/about
```

Viola!  Again, you can also acces the Ariadne GraphiQL (interactive test playground) instance at [http://localhost:$API_PORT/$ENV/playground](http://localhost:$PLAYGROUND_PORT/$ENV/playground).  

## Testing

The project includes BDD-style tests organized for improved readability and comprehension. These tests are segmented into individual files, a structure that simplifies the testing process and enhances accessibility. While individual preferences may vary, this is my chosen approach for managing tests in this project.

To run the tests, simply enter the following command in your terminal:

```bash
./run_tests.sh
```

## Troubleshooting

### Docker image

To troubleshoot issues with the Docker image used for deployment, build it by executing the following:

```bash
docker build -t py-hotel-res:latest .
docker run --name py-hotel-dev --network host py-hotel-res
```

If the container is running, you should be able to navigate to [http://localhost/development/about](http://localhost/development/about)


To troubleshoot further, you can review files on the container by logging into it:

```bash
CONTAINER_ID=$(docker ps -qf "name=py-hotel-dev" -n 1)
docker exec -it $CONTAINER_ID sh
```

When done, stop the container and then remove it:

```bash
docker stop py-hotel-dev
docker rm py-hotel-dev
```

## License

License information can be found [here](./LICENSE)

