import requests
import urllib3


class MediatorRegistration:
    def __init__(self, **kwargs):
        self.options = kwargs['options']
        self.conf = kwargs['conf']
        self.auth = kwargs['auth']
    
    def run(self):
        self.auth.authenticate()

        if not self.options['verify_cert']:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )
        
        resp = requests.post(
            url=self.options['mediators_url'],
            json=self.conf,
            headers=self.auth.gen_auth_headers(),
            verify=self.options['verify_cert']
        )

        if resp.status_code == 401:
            raise Exception("Authentication failed")
        
        if resp.status_code != 201:
            raise Exception(
                "Received a non-201 response code, the response code was: {}".format(resp.status_code)
            )

