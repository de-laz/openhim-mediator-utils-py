import unittest
import datetime

from unittest import mock
from openhim_mediator_utils.mediator_registration import MediatorRegistration

DISABLE_WARNINGS_PATCH = 'urllib3.disable_warnings'
REQUESTS_POST_PATCH = 'requests.post'


class Run(unittest.TestCase):
    def setUp(self):
        self.options = {
            'verify_cert': False,
            'mediators_url': 'https://localhost/mediators',
        }
        self.conf = {
            "urn": "urn:uuid:3332e057-2ef5-4586-a437-105c9916147f",
            "version": "test-version",
            "name": "OpenHIM Python Mediator",
            "description": "An openHIM python mediator",
            "endpoints": []
        }
        self.registration = MediatorRegistration(
            options=self.options,
            auth=self._get_mock_auth(),
            conf=self.conf
        )

    @mock.patch(REQUESTS_POST_PATCH)
    def test_always_authenticates_with_openHIM(self, mock_post):
        # arrange
        mock_post.return_value = self._get_mock_response()
        
        # act
        self.registration.run()
        
        # assert
        self.assertTrue(self.registration.auth.authenticate.called)
    
    @mock.patch(DISABLE_WARNINGS_PATCH)
    @mock.patch(REQUESTS_POST_PATCH)
    def test_disables_ssl_warnings_when_verify_cert_is_false(self, mock_post, mock_disable_warnings):
        # arrange
        mock_post.return_value = self._get_mock_response()
        
        # act
        self.registration.run()
        
        # assert
        self.assertTrue(mock_disable_warnings.called)

    @mock.patch(DISABLE_WARNINGS_PATCH)
    @mock.patch(REQUESTS_POST_PATCH)
    def test_does_not_disable_ssl_warnings_when_verify_cert_is_true(self, mock_post, mock_disable_warnings):
        # arrange
        mock_post.return_value = self._get_mock_response()
        self.registration.options['verify_cert'] = True

        # act
        self.registration.run()

        # assert
        self.assertFalse(mock_disable_warnings.called)
    
    @mock.patch(REQUESTS_POST_PATCH)
    def test_raises_exception_when_response_code_is_401(self, mock_requests_post):
        # arrange
        mock_requests_post.return_value = self._get_mock_response(status=401)
        self.registration.options['verify_cert'] = True
        
        # assert
        self.assertRaises(Exception, self.registration.run)
    
    @mock.patch(REQUESTS_POST_PATCH)
    def test_raises_exception_when_response_code_is_not_201(self, mock_request_post):
        # arrange
        mock_request_post.return_value = self._get_mock_response(status=200)
        self.registration.options['verify_cert'] = True
        
        # assert
        self.assertRaises(Exception, self.registration.run)

    @staticmethod
    def _get_mock_auth():
        mock_auth = mock.Mock()
        mock_auth.authenticate.return_value = None
        mock_auth.gen_auth_headers.return_value = {
            'auth-username': 'username',
            'auth-ts': str(datetime.datetime.utcnow()),
            'auth-salt': 'some salt',
            'auth-token': 'and a token'
        }
        return mock_auth
    
    @staticmethod
    def _get_mock_response(status=201, content='Body', json_data=None):
        mock_response = mock.Mock()
        mock_response.status_code = status
        mock_response.content = content

        if json_data:
            mock_response.json = mock.Mock(return_value=json_data)

        return mock_response


if __name__ == '__main__':
    unittest.main()
