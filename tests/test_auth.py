import unittest

from datetime import datetime
from unittest import mock
from openhim_mediator_utils.auth import Auth


API_URL = 'https://localhost:8080'
USERNAME = 'user'


class Authenticate(unittest.TestCase):
    def setUp(self):
        self.auth = Auth({'verify_cert': False, 'apiURL': API_URL, 'username': USERNAME})

    @mock.patch('urllib3.disable_warnings')
    @mock.patch('requests.get')
    def test_disables_ssl_warnings_when_verify_cert_is_false(self, mock_get, mock_disable_warnings):
        # arrange
        mock_get.return_value = self._get_mock_response(
            status=200,
            content='Sample content',
            json_data={'salt': 'some salt'}
        )
        
        # act
        self.auth.authenticate()
        
        # assert
        self.assertTrue(mock_disable_warnings.called)
    
    @mock.patch('urllib3.disable_warnings')
    @mock.patch('requests.get')
    def test_does_not_disable_ssl_warnings_when_verify_cert_is_true(self, mock_get, mock_disable_warnings):
        # arrange
        self.auth.options['verify_cert'] = True
        mock_get.return_value = self._get_mock_response(
            status=200,
            content='Sample content',
            json_data={'salt': 'some salt'}
        )

        # act
        self.auth.authenticate()

        # assert
        self.assertFalse(mock_disable_warnings.called)

    @mock.patch('requests.get')
    def test_raises_exception_when_response_code_is_not_200(self, mock_get):
        # arrange
        mock_get.return_value = self._get_mock_response(
            status=500,
            content='Internal Server Error',
            json_data={'salt': 'some salt'}
        )
        
        # assert
        self.assertRaises(Exception, self.auth.authenticate)
    
    @mock.patch('requests.get')
    def test_sets_salt_when_request_succeeds(self, mock_get):
        # arrange
        mock_get.return_value = self._get_mock_response(
            status=200,
            content='Internal Server Error',
            json_data={'salt': 'some salt'}
        )
        
        # act
        body = self.auth.authenticate()
        
        # assert
        self.assertEqual(body['salt'], 'some salt')

    @staticmethod
    def _get_mock_response(status=200, content='Body', json_data=None):
        mock_response = mock.Mock()
        mock_response.status_code = status
        mock_response.content = content

        if json_data:
            mock_response.json = mock.Mock(return_value=json_data)

        return mock_response


class GenAuthHeaders(unittest.TestCase):
    def test_raises_exception_when_no_salt(self):
        # arrange
        auth = Auth(None)
        
        # assert
        self.assertRaises(Exception, auth.gen_auth_headers)
    
    @mock.patch('hashlib.sha512')
    @mock.patch('datetime.datetime')
    def test_returns_correct_headers_when_no_exceptions(self, fake_datetime, fake_sha512):
        # arrange
        auth = Auth({'username': USERNAME, 'password': 'password'})
        auth.salt = 'random salt'
        fake_date = str(datetime.utcnow())
        fake_datetime.utcnow.return_value = fake_date
        expected_token = 'this is a test token'
        fake_sha512.return_value = self._get_mock_sha512(expected_token)
        
        # act
        result = auth.gen_auth_headers()
        
        # assert
        self.assertIn('auth-username', result.keys())
        self.assertEqual(result['auth-username'], USERNAME)
        self.assertIn('auth-ts', result.keys())
        self.assertEqual(result['auth-ts'], fake_date)
        self.assertIn('auth-salt', result.keys())
        self.assertEqual(result['auth-salt'], auth.salt)
        self.assertIn('auth-token', result.keys())
        self.assertEqual(result['auth-token'], expected_token)

    @staticmethod
    def _get_mock_sha512(token=None):
        mock_sha512 = mock.Mock()
        mock_sha512.hexdigest.return_value = token
        mock_sha512.update.return_value = None
        return mock_sha512


if __name__ == '__main__':
    unittest.main()
