import os
from dotenv import load_dotenv

load_dotenv()


class PostgreSQLConfig:
    name = os.getenv('POSTGRES_DB', 'backendnapoleonit')
    user = os.getenv('POSTGRES_USER', 'admin')
    password = os.getenv('POSTGRES_PASSWORD', 'auf')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    url = rf'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'