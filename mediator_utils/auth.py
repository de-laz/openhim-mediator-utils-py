import requests
import json
import hashlib

from datetime import datetime

class Auth:
    def __init__(self, options):
        self.options = options
        self.salt = ''

    def authenticate(self):
        result = requests.get(
            f"{self.options['apiURL']}/authenticate/{self.options['username']}",
            verify=self.options['verify']
        )

        if result.status_code != 200:
            raise Exception(f"User {self.options} not found when authenticating with core API")
        
        body = result.json()
        self.salt = body['salt']
        return body

    
    def gen_auth_headers(self):
        if not self.salt:
            raise Exception(
                f"{self.options['username']} has not been authenticated. Please use the .authenticate() function first"
            )
        
        shasum = hashlib.sha512()
        shasum.update(f"{self.salt + self.options['password']}".encode('utf-8'))
        password_hash = shasum.hexdigest()

        shasum = hashlib.sha512()
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        shasum.update(f"{password_hash + self.salt + now}".encode('utf-8'))
        token = shasum.hexdigest()
        
        return {
            'auth-username': self.options['username'],
            'auth-ts': now,
            'auth-salt': self.salt,
            'auth-token': token
        }

