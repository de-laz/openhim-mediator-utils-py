class Heartbeat:
    def __init__(self, auth, **kwargs):
        self.auth = auth
        self.force_config = kwargs['force_config']
        self.options = kwargs['options']
    
    def send(self):
        pass
    
    def activate(self):
        pass
    
    def deactivate(self):
        pass
    
    def fetch_config(self):
        pass
