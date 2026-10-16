"""Conexão com o PostgreSQL compartilhada por ingest.py e dashboard.py."""
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine


def get_engine():
    """Cria o engine SQLAlchemy a partir de variáveis de ambiente.

    Os valores padrão batem com o docker-compose.yml, então o projeto
    roda sem configurar nada.
    """
    user = os.getenv("POSTGRES_USER", "iot_user")
    password = quote_plus(os.getenv("POSTGRES_PASSWORD", "iot_pass"))
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "iot_db")
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url)
