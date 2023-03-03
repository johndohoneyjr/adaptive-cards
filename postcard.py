import os
import requests
import json
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from adaptivecards.adaptivecard import AdaptiveCard
from adaptivecards.elements import TextBlock
from adaptivecards.containers import Column, ColumnSet, Container

def generate_adaptive_card():
    # Opening JSON file
    with open('./json/postbody_template.json') as json_file:
      adapterPost = json.load(json_file)

    card = AdaptiveCard()
    card.body = [
        Container(items=[
            TextBlock(text='Hello from adaptivecards and Python using Pypi AdaptiveCards', font_type='Default', size='Medium'),
            ColumnSet(columns=[
                Column(
                    width='stretch',
                    items=[
                        TextBlock(text='author', weight="Bolder", wrap=True),
                        TextBlock(text='version', weight="Bolder", wrap=True),
                    ]
                ),
                Column(
                    width='stretch',
                    items=[
                        TextBlock(text='Superman with his Python--is this test done yet', wrap=True),
                        TextBlock(text='0.1.0', wrap=True),
                    ]
                )
            ])
        ]),
        TextBlock(text='more information can be found at [https://pypi.org/project/adaptivecards/](https://pypi.org/project/adaptivecards/)',
                  wrap=True)
    ]
    json_str = str(card).replace("\n", "")
    card_dict = json.loads(json_str)
    #Splice on the adaptive card with the attachment for the post body
    adapterPost['attachments'][0]['content']['body'][0] = card_dict['body'][0]

    json_object = json.dumps(adapterPost, indent = 4)
    return json_object


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

# The adaptive card JSON file
card = generate_adaptive_card();

# Convert the card to a string
card_str = json.dumps(card)
# remove  \\n characters from the string, clean up formatting in general for POST body JSON
card_str = card_str.replace("\\n", "").replace('\\"','"').replace('"{','{').replace('}"','}') 

# Send a POST request with the card as the body
response = requests.post(webhook_url, data=card_str, headers={"Content-Type": "application/json"})

# Print the status code
print(response.status_code)
