import asyncio
from logging.config import fileConfig

from sqlalchemy import pool, engine_from_config
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.core.config import get_database_url

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

def is_async_postgres_url(url: str) -> bool:
    """Determine if the URL scheme indicates async PostgreSQL."""
    return url.startswith("postgresql+asyncpg://")

# Determine if we are in async mode based on the URL scheme
DATABASE_URL_ASYNC = get_database_url(async_mode=True)
print("DATABASE URL ASYNC: ", DATABASE_URL_ASYNC)
is_async_connection = is_async_postgres_url(DATABASE_URL_ASYNC)
# DB Connection configuration
config.set_main_option('sqlalchemy.url', DATABASE_URL_ASYNC)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection, target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online_async() -> None:
    """Run migrations in 'online' mode using asyncio."""
    connectable = create_async_engine(
        config.get_main_option('sqlalchemy.url'),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations_online_sync() -> None:
    """Run migrations in 'online' mode using synchronous connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    if is_async_connection:
        asyncio.run(run_migrations_online_async())
    else:
        run_migrations_online_sync()