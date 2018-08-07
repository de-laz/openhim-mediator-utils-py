import requests
import hashlib
import urllib3
import datetime


class Auth:
    def __init__(self, options):
        self.options = options
        self.salt = ''

    def authenticate(self):
        if not self.options['verify_cert']:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

        result = requests.get(
            "{}/authenticate/{}".format(
                self.options['apiURL'],
                self.options['username']
            ),
            verify=self.options['verify_cert']
        )

        if result.status_code != 200:
            raise Exception(
                "User {} not found when authenticating with core API".format(self.options['username'])
            )

        body = result.json()
        self.salt = body['salt']
        return body

    def gen_auth_headers(self):
        if not self.salt:
            raise Exception(
                "{} has not been authenticated. Please use the .authenticate() function first".format(
                    self.options['username']
                )
            )

        sha = hashlib.sha512()
        sha.update((self.salt + self.options['password']).encode('utf-8'))
        password_hash = sha.hexdigest()

        sha = hashlib.sha512()
        now = str(datetime.datetime.utcnow())
        sha.update((password_hash + self.salt + now).encode('utf-8'))
        token = sha.hexdigest()

        return {
            'auth-username': self.options['username'],
            'auth-ts': now,
            'auth-salt': self.salt,
            'auth-token': token
        }
