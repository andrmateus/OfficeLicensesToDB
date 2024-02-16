# models/database.py

from config.config import servidor, user, password, tabela_destino, database_destino
from sqlalchemy import create_engine
import pandas as pd


def enviar_para_banco(df: pd.DataFrame):
    engine = create_engine(f"mysql+mysqldb://{user}:{password}@{servidor}/{database_destino}")

    df.to_sql(tabela_destino, con=engine, if_exists="replace", index=False)
    return True
