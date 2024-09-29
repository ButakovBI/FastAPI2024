from datetime import datetime
from sqlalchemy import MetaData, Table, Integer, Column, String, TIMESTAMP, ForeignKey, JSON


metadata = MetaData()

roles = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

users = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("fullname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("register_data", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey("role.id")),
)