import requests
from urllib.parse import urlencode, urlparse, parse_qs

# Salla OAuth endpoints
authorization_url = "https://accounts.salla.sa/oauth2/auth"
token_url = "https://accounts.salla.sa/oauth2/token"

# Your Salla App credentials
client_id = ''  # Your Salla App client ID
client_secret = ''  # Your Salla App client secret
redirect_uri = ''  # Your Salla App redirect URI
scope = "offline_access"  # Scope for the OAuth request

# Define state_param globally
# Update the state_param variable with a random value
state_param = "8rnzqtXPDLNOkTu9syaCEzB4"

# Store used authorization codes
used_codes = set()

def generate_authorization_url():
    # Step 1: Generate the authorization URL
    authorization_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state_param,
    }
    return f"{authorization_url}?{urlencode(authorization_params)}"

def exchange_code_for_token(authorization_code):
    # Step 3: Exchange the authorization code for an access token
    if authorization_code in used_codes:
        print("Authorization code has already been used.")
        return

    token_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }

    response = requests.post(token_url, data=token_params)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Access Token:", access_token)
        # Mark the code as used
        used_codes.add(authorization_code)
    else:
        print(f"Failed to obtain access token: {response.json()}")
        print("Full response:", response.text)

# Step 1: Generate the authorization URL
authorization_url_with_params = generate_authorization_url()
print("Visit this URL to authorize your app:", authorization_url_with_params)

# Step 2: Handle the callback URL after authorization
callback_url = input("Enter the callback URL after authorization: ")

# Parse the callback URL to extract the authorization code and state
parsed_url = urlparse(callback_url)
query_params = parse_qs(parsed_url.query)
authorization_code = query_params.get("code", [None])[0]
received_state = query_params.get("state", [None])[0]

if received_state is None or received_state != state_param:
    print("Error: The received state does not match the expected state.")
else:
    print("Authorization Code:", authorization_code)

    # Step 3: Exchange the authorization code for an access token
    exchange_code_for_token(authorization_code)
