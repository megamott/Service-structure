from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from app.configuration.config import get_settings
from app.configuration.database_accessor import DatabaseAccessor
from app.models import db

config = context.config
fileConfig(config.config_file_name)
target_metadata = db


def run_migrations_online():

    config = get_settings()
    DatabaseAccessor()
    
    connectable = create_engine(config.database_url)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
