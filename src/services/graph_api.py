# services/graph_api.py
import requests
from io import BytesIO
import pandas as pd
from config.config import tenant_id, client_id, client_secret

def get_token():
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def buscar_relatorio(operacao):
    access_token = get_token()
    url = f"https://graph.microsoft.com/v1.0/reports/{operacao}(period='D180')"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.request("GET", url, headers=headers)
    content = BytesIO(response.content)
    df = pd.read_csv(content) 
    return df