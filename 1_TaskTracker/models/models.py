from datetime import datetime, timezone
from sqlalchemy import MetaData, Table, Integer, Serial, Boolean, Column, String, TIMESTAMP, ForeignKey, Text

metadata = MetaData()

tasks = Table(
    "Task",
    metadata,
    Column("id", Serial, primary_key=True),
    Column("title", Text, nullable=False),
    Column("description", Text, nullable=False, default=""),
    Column("start_date", TIMESTAMP, nullable=False, default=datetime.now(timezone.utc)),
    Column("end_date", TIMESTAMP, nullable=False, default="3000-01-01"),
    Column("done", Boolean, nullable=False, default=False),
)

users = Table(
    "User",
    metadata,
    Column("id", Serial, primary_key=True),
    Column("task_id", Integer, ForeignKey("task.id")),
    Column("name", Text, nullable=False),
    Column("password", Text, nullable=False),
)