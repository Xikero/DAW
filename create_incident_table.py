from app import create_app, db
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, MetaData

app = create_app()
with app.app_context():
    meta = MetaData()

    incident = Table(
        'incident', meta,
        Column('id', Integer, primary_key=True),
        Column('project', String(100), nullable=False),
        Column('description', Text, nullable=False),
        Column('position', String(100), nullable=False),
        Column('responsible', String(100), nullable=False),
        Column('status', String(100), nullable=False),
        Column('created_by', String(100), nullable=False),
        Column('created_at', DateTime, nullable=False),
    )

    meta.create_all(db.engine)
    print("Tables created successfully.")
