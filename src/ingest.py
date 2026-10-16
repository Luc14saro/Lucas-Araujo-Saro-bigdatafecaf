"""Ingestão: lê o CSV do Kaggle, limpa os dados e carrega no PostgreSQL.

Dataset: "Temperature Readings: IoT Devices" (atulanandjha)
Colunas originais: id, room_id/id, noted_date, temp, out/in

Uso:
    python src/ingest.py                      # usa data/IOT-temp.csv
    python src/ingest.py --csv caminho.csv
"""
import argparse
import pathlib
import sys

import pandas as pd
from sqlalchemy import text

from db import get_engine

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CSV_PADRAO = RAIZ / "data" / "IOT-temp.csv"
VIEWS_SQL = RAIZ / "sql" / "views.sql"

DDL = """
DROP TABLE IF EXISTS temperature_readings CASCADE;
CREATE TABLE temperature_readings (
    id          SERIAL PRIMARY KEY,
    reading_id  TEXT,
    device_id   TEXT        NOT NULL,
    noted_date  TIMESTAMP   NOT NULL,
    temperature NUMERIC(5,2) NOT NULL,
    location    TEXT
);
"""


def ler_e_limpar(caminho: pathlib.Path) -> pd.DataFrame:
    """Lê o CSV, renomeia colunas, converte tipos e remove sujeira."""
    df = pd.read_csv(caminho)
    print(f"Linhas lidas do CSV: {len(df)}")

    df = df.rename(
        columns={
            "id": "reading_id",
            "room_id/id": "device_id",
            "noted_date": "noted_date",
            "temp": "temperature",
            "out/in": "location",
        }
    )

    # O CSV usa o formato dia-mês-ano hora:minuto (ex.: 08-12-2018 09:30)
    df["noted_date"] = pd.to_datetime(
        df["noted_date"], format="%d-%m-%Y %H:%M", errors="coerce"
    )
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["location"] = df["location"].astype(str).str.strip().str.title()

    # Remove linhas inválidas e duplicadas
    antes = len(df)
    df = df.dropna(subset=["device_id", "noted_date", "temperature"])
    df = df.drop_duplicates(subset=["reading_id"])
    print(f"Linhas removidas (nulas/duplicadas): {antes - len(df)}")

    return df[["reading_id", "device_id", "noted_date", "temperature", "location"]]


def carregar(df: pd.DataFrame) -> None:
    """Cria a tabela, insere os dados e cria as views."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(DDL))
    df.to_sql(
        "temperature_readings",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000,
    )
    with engine.begin() as conn:
        conn.execute(text(VIEWS_SQL.read_text(encoding="utf-8")))
        total = conn.execute(text("SELECT COUNT(*) FROM temperature_readings")).scalar()
    print(f"Linhas no PostgreSQL: {total}")
    print("Views criadas: avg_temp_por_dispositivo, leituras_por_hora, temp_max_min_por_dia")


def main() -> int:
    parser = argparse.ArgumentParser(description="Carga do CSV de temperaturas IoT")
    parser.add_argument("--csv", type=pathlib.Path, default=CSV_PADRAO)
    args = parser.parse_args()

    if not args.csv.exists():
        print(
            f"CSV não encontrado em {args.csv}.\n"
            "Baixe em https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices "
            "e salve como data/IOT-temp.csv"
        )
        return 1

    carregar(ler_e_limpar(args.csv))
    return 0


if __name__ == "__main__":
    sys.exit(main())
