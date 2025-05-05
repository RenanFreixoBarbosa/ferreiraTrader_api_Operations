import os
import json
import requests
import jwt
import time
from google.oauth2 import service_account
import google.auth.transport.requests

class GooglePlayServices:
    def __init__(self, package_name: str, product_id: str):
        self.package_name = package_name
        self.product_id = product_id

    def get_credentials(self) -> dict:
        credentials_token = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        scope= os.getenv("GOOGLE_CREDENTIALS")
        credentials = service_account.Credentials.from_service_account_file(credentials_token, scopes=[scope])
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)

        # Exibe o token
        print("Access Token:", credentials.token)

        return credentials.token


    def _obter_token_acesso(self) -> str | None:
        # ... (seu código para obter o token de acesso, usando self.credentials)
        token_url = self.credentials.get("token_uri")
        client_email = self.credentials.get("client_email")
        private_key = self.credentials.get("private_key")

        if not all([token_url, client_email, private_key]):
            print("Erro: Informações de credenciais incompletas nas variáveis de ambiente.")
            return None

        payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": self._montar_assertion(client_email, private_key, token_url)
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(token_url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter token de acesso: {e}")
            return None

    def _montar_assertion(self, client_email: str, private_key: str, token_url: str) -> str:
        now = int(time.time())
        payload = {
            "iss": client_email,
            "scope": "https://www.googleapis.com/auth/androidpublisher",
            "aud": token_url,
            "exp": now + 3600,
            "iat": now
        }
        return jwt.encode(payload, private_key, algorithm="RS256")

    def check_sub(self, purchase_token: str) -> dict | None:
        '''
            Verifica se a compra é válida e retorna um json e um condição booleana informando se a assinatura é válida ou não.
            Em caso da assinatura não for válida, retorna None e False.
        '''
        if not self.access_token:
            print("Erro: Token de acesso não disponível.")
            return None,False

        url = f"https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{self.package_name}/purchases/products/{self.product_id}/tokens/{purchase_token}"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(),True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao verificar compra: {e}")
            return None,False
        
    def webhook_goole(self):...
