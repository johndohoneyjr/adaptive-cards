import os
import requests
import json
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import pymsteams

# The Azure AD tenant ID
tenant_id = os.environ.get("PT_TENANT_ID")
# The Azure AD client ID
client_id = os.environ.get("PT_CLIENT_ID")
# The Azure AD client secret
client_secret = os.environ.get("PT_CLIENT_SECRET")
# The Azure Key Vault name
vault_name = "code-translation-kv"

# Create a credential object using MSAL for Python
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Create a secret client object using azure-keyvault-secrets library
secret_client = SecretClient(vault_url=f"https://{vault_name}.vault.azure.net", credential=credential)

# Retrieve the webhook URL from Azure Key Vault
secret = secret_client.get_secret("webhook-url")
webhook_url = secret.value



# You must create the connectorcard object with the Microsoft Webhook URL
myTeamsMessage = pymsteams.connectorcard(webhook_url)

# Add text to the message.
myTeamsMessage.text("this is a message from pymsteams")

# send the message.
myTeamsMessage.send()
