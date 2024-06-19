import unittest
from unittest.mock import patch, Mock
from commands.manage_user import sync_user
from data_.models import GitHubUser


class TestMainFunction(unittest.TestCase):

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
        self.mock_get_github_user_patcher = patch('commands.manage_user.get_github_user')
        self.mock_create_or_update_contact_patcher = patch('commands.manage_user.create_or_update_contact')
        self.mock_read_query_patcher = patch('commands.manage_user.read_query')
        self.mock_insert_query_patcher = patch('commands.manage_user.insert_query')
        self.mock_update_query_patcher = patch('commands.manage_user.update_query')

        self.mock_get_github_user = self.mock_get_github_user_patcher.start()
        self.mock_create_or_update_contact = self.mock_create_or_update_contact_patcher.start()
        self.mock_read_query = self.mock_read_query_patcher.start()
        self.mock_insert_query = self.mock_insert_query_patcher.start()
        self.mock_update_query = self.mock_update_query_patcher.start()

        self.mock_github_user = GitHubUser(**self.mock_github_user_data)

    def tearDown(self):
        self.mock_get_github_user_patcher.stop()
        self.mock_create_or_update_contact_patcher.stop()
        self.mock_read_query_patcher.stop()
        self.mock_insert_query_patcher.stop()
        self.mock_update_query_patcher.stop()

    def test_syncUser_createsContact(self):
        # Arrange
        self.mock_get_github_user.return_value = self.mock_github_user
        self.mock_create_or_update_contact.return_value = "Created new contact Bojigol (ikonata@github.com)"
        self.mock_read_query.return_value = []

        # Act
        result = sync_user("ikonata", "fake_subdomain")

        # Assert
        self.assertEqual(result, "Created new contact Bojigol (ikonata@github.com)")
        self.mock_get_github_user.assert_called_once_with("ikonata")
        self.mock_create_or_update_contact.assert_called_once()
        self.mock_insert_query.assert_called_once()

    def test_syncUser_User_notFound(self):
        # Arrange
        self.mock_get_github_user.side_effect = Exception("404 Not Found")

        # Act & Assert
        with self.assertRaises(Exception) as context:
            sync_user("ikonataismissing", "fake_subdomain")
        self.assertEqual(str(context.exception), "404 Not Found")
        self.mock_get_github_user.assert_called_once_with("ikonataismissing")

    def test_syncUser_when_emailIsPrivate(self):
        # Arrange
        github_user_data_with_private_email = self.mock_github_user_data.copy()
        github_user_data_with_private_email['email'] = None
        self.mock_get_github_user.return_value = GitHubUser(**github_user_data_with_private_email)
        self.mock_create_or_update_contact.return_value = "Email is Private or None, can't create a new contact!"
        self.mock_read_query.return_value = []

        # Act
        result = sync_user("ikonata", "fake_subdomain")

        # Assert
        self.assertEqual(result, "Email is Private or None, can't create a new contact!")
        self.mock_get_github_user.assert_called_once_with("ikonata")
        self.mock_insert_query.assert_called_once()
        self.mock_update_query.assert_not_called()

    def test_syncUser_updatesContact(self):
        # Arrange
        self.mock_get_github_user.return_value = self.mock_github_user
        self.mock_create_or_update_contact.return_value = "Updated contact Bojigol (ikonata@github.com)"
        self.mock_read_query.return_value = [("ikonata",)]

        # Act
        result = sync_user("ikonata", "fake_subdomain")

        # Assert
        self.assertEqual(result, "Updated contact Bojigol (ikonata@github.com)")
        self.mock_get_github_user.assert_called_once_with("ikonata")
        self.mock_create_or_update_contact.assert_called_once()
        self.mock_update_query.assert_called_once()
        self.mock_insert_query.assert_not_called()


if __name__ == '__main__':
    unittest.main()






