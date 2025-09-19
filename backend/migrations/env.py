from __future__ import annotations
import os, sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine, pool

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config as app_config
from extensions import db

# import models so autogenerate sees the tables
from auth.models import User  # noqa
from clients.models import Client  # noqa
from documents.models import Document  # noqa
from tasks.models import Task, TaskComment  # noqa
from audit.models import ActivityLog  # noqa

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = db.metadata

def get_url() -> str:
    return os.getenv("DATABASE_URL", app_config.SQLALCHEMY_DATABASE_URI)

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(get_url(), poolclass=pool.NullPool, future=True)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
