# src/main.py
import pandas as pd
from services.graph_api import buscar_relatorio
from models.database import enviar_para_banco

# Supondo que o processamento e a lógica de merge sejam mantidos aqui, você pode chamar as funções definidas em outros arquivos:
mailbox_usage = buscar_relatorio("getMailboxUsageDetail")
office_usage = buscar_relatorio("getOffice365ActiveUserDetail")
onedrive_usage = buscar_relatorio("getOneDriveUsageAccountDetail")

# Processamento dos dados e merge (continuação do seu script...)
office_usage = office_usage[
    [
        "Report Refresh Date",
        "User Principal Name",
        "Display Name",
        "Is Deleted",
        "Has Exchange License",
        "Exchange License Assign Date",
        "Exchange Last Activity Date",
        "Teams Last Activity Date",
        "Assigned Products",
    ]
]
office_usage = office_usage.rename(
    columns={"Report Refresh Date": "Report Refresh Date Office Use"}
)
mailbox_usage = mailbox_usage[
    [
        "Report Refresh Date",
        "User Principal Name",
        "Last Activity Date",
        "Storage Used (Byte)",
    ]
]
mailbox_usage = mailbox_usage.rename(
    columns={
        "Report Refresh Date": "Report Refresh Date Mailbox",
        "Storage Used (Byte)": "Storage Mailbox Used (Byte)",
    }
)
merge1 = pd.merge(
    office_usage,
    mailbox_usage,
    how="left",
    left_on="User Principal Name",
    right_on="User Principal Name",
)

onedrive_usage = onedrive_usage[
    [
        "Report Refresh Date",
        "Owner Principal Name",
        "Storage Used (Byte)",
        "Storage Allocated (Byte)",
    ]
]
onedrive_usage = onedrive_usage.rename(
    columns={
        "Report Refresh Date": "Report Refresh Date OneDrive",
        "Storage Used (Byte)": "Storage Onedrive Used (Byte)",
        "Storage Allocated (Byte)": "Storage Onedrive Allocated (Byte)",
    }
)
merge2 = pd.merge(
    merge1,
    onedrive_usage,
    how="left",
    left_on="User Principal Name",
    right_on="Owner Principal Name",
)

final = merge2[
    [
        "Report Refresh Date Office Use",
        "User Principal Name",
        "Display Name",
        "Is Deleted",
        "Has Exchange License",
        "Exchange License Assign Date",
        "Exchange Last Activity Date",
        "Teams Last Activity Date",
        "Assigned Products",
        "Report Refresh Date Mailbox",
        "Last Activity Date",
        "Storage Mailbox Used (Byte)",
        "Report Refresh Date OneDrive",
        "Storage Onedrive Used (Byte)",
        "Storage Onedrive Allocated (Byte)",
    ]
]

enviar_para_banco(final)