import unittest
from unittest.mock import patch, Mock
from services.github_service import get_github_user
from data_.models import GitHubUser
import os

class TestGitHubService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_github_user_data = {
            "login": "ikonata",
            "name": "Bojigol",
            "company": "BFS",
            "location": "Universe",
            "email": "ikonata@github.com",
            "html_url": "https://github.com/ikonata",
            "bio": "Loves little cats",
            "twitter_username": "ikonata"
        }

    def setUp(self):
        self.mock_get_patcher = patch('services.github_service.requests.get')
        self.mock_get = self.mock_get_patcher.start()
        self.addCleanup(self.mock_get_patcher.stop)

        self.original_github_token = os.environ.get('GITHUB_TOKEN')
        os.environ['GITHUB_TOKEN'] = 'fake_github_token'

    def tearDown(self):
        if self.original_github_token is not None:
            os.environ['GITHUB_TOKEN'] = self.original_github_token
        elif 'GITHUB_TOKEN' in os.environ:
            del os.environ['GITHUB_TOKEN']

    def test_get_GitHub_User_success(self):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = self.mock_github_user_data
        mock_response.raise_for_status = Mock()
        self.mock_get.return_value = mock_response

        # Act
        result = get_github_user("ikonata")

        # Assert
        self.assertEqual(result, GitHubUser(**self.mock_github_user_data))
        self.mock_get.assert_called_once_with("https://api.github.com/users/ikonata", headers={'Authorization': 'token fake_github_token'})

    def test_get_GitHub_User_notFound(self):
        # Arrange
        self.mock_get.return_value.raise_for_status.side_effect = Exception("404 Not Found")

        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_github_user("ikonataismissing")
        self.assertEqual(str(context.exception), "404 Not Found")
        self.mock_get.assert_called_once_with("https://api.github.com/users/ikonataismissing", headers={'Authorization': 'token fake_github_token'})

    def test_get_GitHub_User_noApiKey(self):
        # Arrange
        del os.environ['GITHUB_TOKEN']

        # Act & Assert
        with self.assertRaises(EnvironmentError) as context:
            get_github_user("ikonata")

        # Assert
        self.assertEqual(str(context.exception), "GITHUB_TOKEN not set in environment variables")

    def test_get_GitHub_User_expiredApiKey(self):
        # Arrange
        self.mock_get.return_value.raise_for_status.side_effect = Exception("401 Unauthorized")

        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_github_user("ikonata")
        self.assertEqual(str(context.exception), "401 Unauthorized")
        self.mock_get.assert_called_once_with("https://api.github.com/users/ikonata", headers={'Authorization': 'token fake_github_token'})

if __name__ == '__main__':
    unittest.main()
