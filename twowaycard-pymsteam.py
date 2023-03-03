import os
import requests
import json
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import pymsteams
import json

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

myTeamsMessage = pymsteams.connectorcard(webhook_url)

myTeamsPotentialAction1 = pymsteams.potentialaction(_name = "Add a comment")
myTeamsPotentialAction1.addInput("TextInput","comment","Add a comment here",False)
myTeamsPotentialAction1.addAction("HttpPost","Add Comment","https://reqbin.com/echo/post/json") 

myTeamsPotentialAction2 = pymsteams.potentialaction(_name = "Set due date")
myTeamsPotentialAction2.addInput("DateInput","dueDate","Enter due date")
myTeamsPotentialAction2.addAction("HttpPost","save","https://reqbin.com/echo/post/json")

myTeamsPotentialAction3 = pymsteams.potentialaction(_name = "Change Status")
myTeamsPotentialAction3.choices.addChoices("In progress","0")
myTeamsPotentialAction3.choices.addChoices("Active","1")
myTeamsPotentialAction3.addInput("MultichoiceInput","list","Select a status",False)
myTeamsPotentialAction3.addAction("HttpPost","Save","https://reqbin.com/echo/post/json")

myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)
myTeamsMessage.addPotentialAction(myTeamsPotentialAction2)
myTeamsMessage.addPotentialAction(myTeamsPotentialAction3)

myTeamsMessage.summary("Options Card - Test Message")

myTeamsMessage.send()