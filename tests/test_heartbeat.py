import unittest

from unittest import mock
from openhim_mediator_utils.heartbeat import Heartbeat


class Activate(unittest.TestCase):
    def setUp(self):
        self.scheduler = mock.Mock()
        self.auth = mock.Mock()
        self.heartbeat = Heartbeat(
            auth=self.auth,
            options={'interval': 5},
            conf=None,
            scheduler=self.scheduler
        )
        self.auth.authenticate.return_value = None
    
    def test_activate_always_authenticates_with_openHIM(self):
        # act
        self.heartbeat.activate()
        
        # assert
        self.assertTrue(self.auth.authenticate.called)
    
    def test_activate_does_not_start_scheduler_when_jobs_is_not_none(self):
        # arrange
        self.heartbeat._Heartbeat__job = mock.Mock()
        
        # act
        self.heartbeat.activate()
        
        # assert
        self.assertFalse(self.scheduler.start.called)
    
    def test_activate_starts_scheduler_when_jobs_is_none(self):
        # arrange
        self.scheduler.add_job.return_value = mock.Mock()
        
        # act
        self.heartbeat.activate()
        
        # assert
        self.assertTrue(self.scheduler.start.called)


class Deactivate(unittest.TestCase):
    def setUp(self):
        self.scheduler = mock.Mock()
        self.auth = mock.Mock()
        self.heartbeat = Heartbeat(
            auth=self.auth,
            options={'interval': 5},
            conf=None,
            scheduler=self.scheduler
        )
        self.auth.authenticate.return_value = None

    def test_removes_job_when_job_is_not_none(self):
        # arrange
        self.heartbeat._Heartbeat__job = mock.Mock()

        # act
        self.heartbeat.deactivate()

        # assert
        self.assertTrue(self.heartbeat._Heartbeat__job.remove.called)


class FetchConfig(unittest.TestCase):
    def setUp(self):
        self.scheduler = mock.Mock()
        self.auth = mock.Mock()
        self.heartbeat = Heartbeat(
            auth=self.auth,
            options={'interval': 5},
            conf=None,
            scheduler=self.scheduler
        )
        self.auth.authenticate.return_value = None
    
    def test_always_authenticates_with_openHIM(self):
        # arrange
        self.heartbeat._send = mock.Mock()
        self.heartbeat._send.return_value = None
        
        # act
        self.heartbeat.fetch_config()
        
        # assert
        self.assertTrue(self.auth.authenticate.called)

    def test_send_heartbeat_with_force_config_true(self):
        # arrange
        self.heartbeat._send = mock.Mock()
        self.heartbeat._send.return_value = None

        # act
        self.heartbeat.fetch_config()

        # assert
        self.heartbeat._send.assert_called_once_with(True)


if __name__ == '__main__':
    unittest.main()
