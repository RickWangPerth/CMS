from django.conf import settings
from urllib.parse import urlencode
import requests

def get_cognito_login_url():
    cognito_domain = settings.COGNITO_DOMAIN
    client_id = settings.COGNITO_CLIENT_ID
    redirect_uri = settings.COGNITO_CALLBACK_URL
    
    query_params = urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'scope': 'openid email phone',
        'redirect_uri': redirect_uri,
    })
    return f"{cognito_domain}/login?{query_params}"

def get_cognito_logout_url():
    cognito_domain = settings.COGNITO_DOMAIN
    client_id = settings.COGNITO_CLIENT_ID
    logout_uri = settings.COGNITO_LOGOUT_URL

    query_params = urlencode({
        'client_id': client_id,
        'logout_uri': logout_uri,
    })
    return f"{cognito_domain}/logout?{query_params}"

def exchange_code_for_tokens(code):
    cognito_domain = settings.COGNITO_DOMAIN
    client_id = settings.COGNITO_CLIENT_ID
    client_secret = settings.COGNITO_CLIENT_SECRET
    redirect_uri = settings.COGNITO_CALLBACK_URL

    token_url = f"{cognito_domain}/oauth2/token"
    payload = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    response.raise_for_status()
