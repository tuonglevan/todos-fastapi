# FastAPI with PostgreSQL using Docker Compose

This project demonstrates how to set up a to-do list application using FastAPI with a PostgreSQL database, all managed through Docker Compose. The application includes the following features:

- **Users**: Manage user accounts, authentication, and profiles.
- **Companies**: Associate users with companies to manage tasks at a corporate level.
- **Tasks**: Create, update, delete, and view tasks, with associations to users and companies.
- **Auth Token**: Secure endpoints with token-based authentication using JWT (JSON Web Tokens).

The setup also includes automatic database migration using Alembic to manage schema changes over time.


## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/tuonglevan/todo-fastapi.git
cd todo-fastapi
```

### 2. Set up environment variables

Create a `.env` file in the root of the project and add the following contents:

```env
POSTGRES_DB=todos
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234567
DEFAULT_PASSWORD_ADMIN=123456
# JWT
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_SECRET_KEY=2334dfdfdfdfdf2334453
JWT_ALGORITHM=HS256
```

### 3. Build and run the application

Use Docker Compose to build and run the application:

```bash
docker-compose up --build
```

This will:

- Build the FastAPI application image.
- Start the PostgreSQL database container.
- Apply database migrations using Alembic.
- Start the FastAPI application.

### 4. Access the application

Once the containers are up and running, you can access the FastAPI application at:

### 5. Stopping the application

To stop the running containers, you can use:

```bash
docker-compose down
```

This will stop and remove the containers defined in the Docker Compose file.
## Useful Commands

### Running Alembic Migrations Manually

If you need to run the Alembic migrations manually (e.g., after modifying models):

```bash
docker-compose run web alembic upgrade head
```

### Creating a new Alembic Migration

To create a new Alembic migration after updating your models:

```bash
docker-compose run web alembic revision  -m "your message"
```

### Downgrading Alembic Migrations

If you need to downgrade migrations, you have a few options:

#### Downgrade by One Revision

To downgrade by one revision:

```bash
docker-compose run web alembic downgrade -1
```

#### Downgrade to a Specific Revision

To downgrade to a specific revision, replace `revision_id` with the target revision ID:

```bash
docker-compose run web alembic downgrade <revision_id>
```

#### Downgrade to Base (Starting Point)

To downgrade all the way back to the base (earliest) state:

```bash
docker-compose run web alembic downgrade base
```