import unittest
from unittest.mock import patch, Mock
from services.freshdesk_service import create_or_update_contact, get_contact_by_id, get_freshdesk_headers
from data_.models import FreshdeskContact
import os

class TestFreshdeskService(unittest.TestCase):

    def setUp(self):
        self.mock_get_patcher = patch('services.freshdesk_service.requests.get')
        self.mock_post_patcher = patch('services.freshdesk_service.requests.post')
        self.mock_put_patcher = patch('services.freshdesk_service.requests.put')
        self.mock_get = self.mock_get_patcher.start()
        self.mock_post = self.mock_post_patcher.start()
        self.mock_put = self.mock_put_patcher.start()
        self.addCleanup(self.mock_get_patcher.stop)
        self.addCleanup(self.mock_post_patcher.stop)
        self.addCleanup(self.mock_put_patcher.stop)

        self.original_freshdesk_token = os.environ.get('FRESHDESK_TOKEN')
        os.environ['FRESHDESK_TOKEN'] = 'fake_freshdesk_token'

        self.mock_freshdesk_contact = FreshdeskContact(
            name="Bojigol",
            email="ikonata@github.com",
            unique_external_id="ikonata",
            job_title="BFS",
            twitter_id="ikonata",
            address="Universe",
            description="GitHub Profile: https://github.com/ikonata\nBio: Loves little cats"
        )

    def tearDown(self):
        if self.original_freshdesk_token is not None:
            os.environ['FRESHDESK_TOKEN'] = self.original_freshdesk_token
        elif 'FRESHDESK_TOKEN' in os.environ:
            del os.environ['FRESHDESK_TOKEN']

    def test_create_contact(self):
        # Arrange
        self.mock_get.return_value.json.return_value = []
        self.mock_get.return_value.status_code = 200
        self.mock_post.return_value.status_code = 201

        # Act
        result = create_or_update_contact(self.mock_freshdesk_contact, "fake_subdomain")

        # Assert
        self.assertEqual(result, f"Created new contact {self.mock_freshdesk_contact.name} ({self.mock_freshdesk_contact.email})")
        self.mock_post.assert_called_once()
        self.mock_put.assert_not_called()

    def test_updateContact(self):
        # Arrange
        mock_existing_contact = {'id': 12345, 'email': self.mock_freshdesk_contact.email}
        self.mock_get.return_value.json.return_value = [mock_existing_contact]
        self.mock_get.return_value.status_code = 200
        self.mock_put.return_value.status_code = 200

        # Act
        result = create_or_update_contact(self.mock_freshdesk_contact, "fake_subdomain")

        # Assert
        self.assertEqual(result, f"Updated contact {self.mock_freshdesk_contact.name} ({self.mock_freshdesk_contact.email})")
        self.mock_put.assert_called_once()
        self.mock_post.assert_not_called()

    def test_createContact_ifPrivateEmail(self):
        # Arrange
        private_email_contact = self.mock_freshdesk_contact.copy(update={"email": None})
        self.mock_get.return_value.json.return_value = []
        self.mock_get.return_value.status_code = 200

        # Act
        result = create_or_update_contact(private_email_contact, "fake_subdomain")

        # Assert
        self.assertEqual(result, "Email is Private or None, can't create a new contact!")
        self.mock_post.assert_not_called()
        self.mock_put.assert_not_called()

    def test_updateContact_ifPrivateEmail(self):
        # Arrange
        mock_existing_contact = {'id': 12345, 'email': self.mock_freshdesk_contact.email}
        self.mock_get.return_value.json.return_value = [mock_existing_contact]
        self.mock_get.return_value.status_code = 200
        self.mock_put.return_value.status_code = 200
        private_email_contact = self.mock_freshdesk_contact.copy(update={"email": None})

        # Act
        result = create_or_update_contact(private_email_contact, "fake_subdomain")

        # Assert
        self.assertEqual(result, f"Updated contact {private_email_contact.name} ({private_email_contact.email})")
        self.mock_put.assert_called_once()
        self.mock_post.assert_not_called()

    def test_getContact_by_existingID(self):
        # Arrange
        mock_existing_contact = {'id': 12345, 'unique_external_id': self.mock_freshdesk_contact.unique_external_id}
        self.mock_get.return_value.json.return_value = [mock_existing_contact]
        self.mock_get.return_value.status_code = 200

        # Act
        result = get_contact_by_id(self.mock_freshdesk_contact.unique_external_id, "fake_subdomain")

        # Assert
        self.assertEqual(result, mock_existing_contact)
        self.mock_get.assert_called_once()

    def test_getContact_if_IdNotFound(self):
        # Arrange
        self.mock_get.return_value.json.return_value = []
        self.mock_get.return_value.status_code = 200

        # Act
        result = get_contact_by_id(self.mock_freshdesk_contact.unique_external_id, "fake_subdomain")

        # Assert
        self.assertIsNone(result)
        self.mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()









