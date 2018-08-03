import requests
import json
import hashlib
import urllib3

from datetime import datetime

class Auth:
    def __init__(self, options):
        self.options = options
        self.salt = ''

    def authenticate(self):
        if self.options['verify_cert'] == False:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

        result = requests.get(
            f"{self.options['apiURL']}/authenticate/{self.options['username']}",
            verify=self.options['verify_cert']
        )

        if result.status_code != 200:
            raise Exception(f"User {self.options['username']} not found when authenticating with core API")
        
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
        now = str(datetime.utcnow())
        shasum.update(f"{password_hash + self.salt + now}".encode('utf-8'))
        token = shasum.hexdigest()
        
        return {
            'auth-username': self.options['username'],
            'auth-ts': now,
            'auth-salt': self.salt,
            'auth-token': token
        }

