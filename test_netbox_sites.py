# filepath: c:\TRABAJO\_TI-Informatica\Empresas\T-Systems\netbox-test\test_netbox_sites.py
"""
Unit tests for netbox_sites.py module.

These tests use mock objects to simulate API responses and test the core functionality
of the NetBoxAPIClient class without requiring an actual NetBox server connection.

To run tests:
    python -m unittest test_netbox_sites.py
"""

import unittest
from unittest.mock import patch, Mock
import json
import sys
import requests

# Import the module to test
from netbox_sites import NetBoxAPIClient, display_sites


class TestNetBoxAPIClient(unittest.TestCase):
    """Test cases for the NetBoxAPIClient class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_url = "http://test-netbox.local"
        self.api_token = "test-token-12345"
        self.client = NetBoxAPIClient(self.base_url, self.api_token)
        
        # Mock API response data
        self.mock_sites_data = {
            "results": [
                {
                    "id": 1,
                    "name": "Test Site 1",
                    "slug": "test-site-1",
                    "status": {"value": "active", "label": "Active"},
                    "description": "Test site 1 description",
                    "url": "http://test-netbox.local/api/dcim/sites/1/"
                },
                {
                    "id": 2,
                    "name": "Test Site 2",
                    "slug": "test-site-2",
                    "status": {"value": "planned", "label": "Planned"},
                    "description": "Test site 2 description",
                    "url": "http://test-netbox.local/api/dcim/sites/2/"
                }
            ]
        }
        
        # Mock status choices data
        self.mock_status_choices = {
            "actions": {
                "POST": {
                    "status": {
                        "choices": [
                            {"value": "active", "display": "Active"},
                            {"value": "planned", "display": "Planned"},
                            {"value": "staging", "display": "Staging"},
                            {"value": "decommissioning", "display": "Decommissioning"},
                            {"value": "retired", "display": "Retired"}
                        ]
                    }
                }
            }
        }

    def test_init(self):
        """Test if the client is initialized correctly with proper URL and headers."""
        self.assertEqual(self.client.base_url, "http://test-netbox.local")
        self.assertEqual(self.client.api_url, "http://test-netbox.local/api/")
        self.assertEqual(self.client.url, "http://test-netbox.local/api/dcim/sites/")
        self.assertEqual(self.client.headers["Authorization"], f"Token {self.api_token}")
        self.assertEqual(self.client.headers["Content-Type"], "application/json")
        self.assertEqual(self.client.headers["Accept"], "application/json")

    @patch('requests.get')
    def test_get_sites_by_status_success(self, mock_get):
        """Test successful API response when getting sites by status."""
        # Configure the mock to return a successful response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.mock_sites_data
        mock_get.return_value = mock_response
        
        # Call the method with a status filter
        sites = self.client.get_sites_by_status(status="active")
        
        # Assert that the expected sites are returned
        self.assertEqual(len(sites), 2)
        self.assertEqual(sites[0]["name"], "Test Site 1")
        self.assertEqual(sites[1]["name"], "Test Site 2")
        
        # Assert that the API was called with correct parameters
        mock_get.assert_called_once_with(
            self.client.url,
            headers=self.client.headers,
            params={"status": "active"}
        )

    @patch('requests.get')
    def test_get_sites_by_status_no_status(self, mock_get):
        """Test API call without specifying a status filter."""
        # Configure the mock
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.mock_sites_data
        mock_get.return_value = mock_response
        
        # Call the method without a status filter
        sites = self.client.get_sites_by_status()
        
        # Assert that the expected sites are returned
        self.assertEqual(len(sites), 2)
        
        # Assert that the API was called with empty params
        mock_get.assert_called_once_with(
            self.client.url,
            headers=self.client.headers,
            params={}
        )

    @patch('requests.get')
    def test_get_sites_by_status_request_error(self, mock_get):
        """Test handling of request errors."""
        # Configure the mock to raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("Test connection error")
        
        # Capture the printed error message
        with patch('builtins.print') as mock_print:
            # Call the method and check that it handles the error gracefully
            sites = self.client.get_sites_by_status(status="active")
            
            # Assert that None is returned on error
            self.assertIsNone(sites)
            
            # Verify that the error was printed
            mock_print.assert_called_once()

    @patch('requests.get')
    def test_get_sites_by_status_json_error(self, mock_get):
        """Test handling of JSON parsing errors."""
        # Configure the mock to return invalid JSON
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = json.JSONDecodeError("Test JSON error", "", 0)
        mock_get.return_value = mock_response
        
        # Capture the printed error message
        with patch('builtins.print') as mock_print:
            # Call the method and check that it handles the error gracefully
            sites = self.client.get_sites_by_status(status="active")
            
            # Assert that None is returned on error
            self.assertIsNone(sites)
            
            # Verify that the error was printed
            mock_print.assert_called_once()

    @patch('requests.options')
    def test_get_available_statuses_success(self, mock_options):
        """Test successful retrieval of available statuses."""
        # Configure the mock
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.mock_status_choices
        mock_options.return_value = mock_response
        
        # Call the method
        statuses = self.client.get_available_statuses()
        
        # Assert that the expected statuses are returned
        self.assertEqual(len(statuses), 5)
        self.assertIn("active", statuses)
        self.assertIn("planned", statuses)
        self.assertIn("staging", statuses)
        self.assertIn("decommissioning", statuses)
        self.assertIn("retired", statuses)

    @patch('requests.options')
    def test_get_available_statuses_error(self, mock_options):
        """Test handling of errors when getting available statuses."""
        # Configure the mock to raise an exception
        mock_options.side_effect = requests.exceptions.RequestException("Test connection error")
        
        # Capture the printed error message
        with patch('builtins.print') as mock_print:
            # Call the method
            statuses = self.client.get_available_statuses()
            
            # Assert that default statuses are returned on error
            self.assertEqual(len(statuses), 5)
            self.assertIn("active", statuses)
            self.assertIn("planned", statuses)
            
            # Verify that the error was printed
            mock_print.assert_called_once()


class TestDisplaySites(unittest.TestCase):
    """Test cases for the display_sites function."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_sites = [
            {
                "id": 1,
                "name": "Test Site 1",
                "slug": "test-site-1",
                "status": {"value": "active", "label": "Active"},
                "description": "Test description 1",
                "url": "http://test-url.com/1"
            },
            {
                "id": 2,
                "name": "Test Site 2",
                "slug": "test-site-2",
                "status": {"value": "planned", "label": "Planned"},
                "description": "Test description 2",
                "url": "http://test-url.com/2"
            }
        ]

    @patch('sys.stdout')
    def test_display_sites_with_status(self, mock_stdout):
        """Test displaying sites with a specific status."""
        # Call the function
        display_sites(self.mock_sites, "active")
        
        # Since we're patching stdout, we can't directly assert the output
        # Instead, we just verify that the function completes without errors

    @patch('sys.stdout')
    def test_display_sites_without_status(self, mock_stdout):
        """Test displaying sites without specifying a status."""
        # Call the function
        display_sites(self.mock_sites)
        
        # Again, just verify that the function completes without errors

    @patch('sys.stdout')
    def test_display_sites_empty_list(self, mock_stdout):
        """Test displaying an empty list of sites."""
        # Call the function
        display_sites([], "active")
        
        # Verify that the function completes without errors


if __name__ == '__main__':
    unittest.main()