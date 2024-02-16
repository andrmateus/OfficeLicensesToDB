# config/config.py
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

servidor = os.getenv("DB_SERVER")
user = os.getenv("DB_USER")
password = quote(os.getenv("DB_PASSWORD"))
tabela_destino = os.getenv("DB_TABLE")
database_destino = os.getenv("DB_NAME")

tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
