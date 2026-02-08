import unittest
from unittest.mock import patch, MagicMock
from get_icd11 import ICD11Client

class TestICD11Client(unittest.TestCase):
    def setUp(self):
        self.client = ICD11Client("test_id", "test_secret")

    @patch('requests.post')
    def test_authenticate_success(self, mock_post):
        # Mock successful authentication
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'fake_token'}
        mock_post.return_value = mock_response

        success = self.client.authenticate()
        
        self.assertTrue(success)
        self.assertEqual(self.client.access_token, 'fake_token')
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_authenticate_failure(self, mock_post):
        # Mock failed authentication
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        success = self.client.authenticate()
        
        self.assertFalse(success)
        self.assertIsNone(self.client.access_token)

    @patch('requests.get')
    @patch('requests.post')
    def test_search_success(self, mock_post, mock_get):
        # Mock authentication
        mock_auth_response = MagicMock()
        mock_auth_response.status_code = 200
        mock_auth_response.json.return_value = {'access_token': 'fake_token'}
        mock_post.return_value = mock_auth_response

        # Mock search result
        mock_search_response = MagicMock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = {
            'destinationEntities': [
                {'theCode': '1A00', 'title': 'Cholera', 'id': 'uri1'},
                {'theCode': '1A01', 'title': 'Typhoid fever', 'id': 'uri2'}
            ]
        }
        mock_get.return_value = mock_search_response

        results = self.client.search("cholera")

        self.assertIsNotNone(results)
        self.assertEqual(len(results['destinationEntities']), 2)
        self.assertEqual(results['destinationEntities'][0]['theCode'], '1A00')
        
        # Verify headers
        headers = mock_get.call_args[1]['headers']
        self.assertEqual(headers['Authorization'], 'Bearer fake_token')
        self.assertEqual(headers['API-Version'], 'v2')

if __name__ == '__main__':
    unittest.main()
