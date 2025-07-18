#!/usr/bin/env python3
"""
Script to query sites in NetBox API by specific status.
Requirements: requests, python-dotenv (optional)
"""

import requests
import json
import sys
from urllib.parse import urljoin
import argparse


class NetBoxAPIClient:
    def __init__(self, base_url, api_token):
        """
        Initialize the NetBox API client

        Args:
            base_url (str): NetBox base URL (e.g., http://localhost:8000)
            api_token (str): NetBox API token
        """
        self.base_url = base_url.rstrip("/")
        self.api_url = urljoin(self.base_url, "/api/")
        # Build endpoint URL
        self.url = urljoin(self.api_url, "dcim/sites/")
        self.headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_sites_by_status(self, status=None):
        """
        Query sites by specific status

        Args:
            status (str): Status to filter (active, planned, decommissioning, etc.)

        Returns:
            list: List of sites that match the status
        """
        try:
            # Query parameters
            params = {}
            if status:
                params["status"] = status

            # Make GET request
            response = requests.get(self.url, headers=self.headers, params=params)
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            return data.get("results", [])

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to NetBox API: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return None

    def get_available_statuses(self):
        """
        Get available statuses for sites

        Returns:
            list: List of available statuses
        """
        try:
            response = requests.options(self.url, headers=self.headers)
            response.raise_for_status()

            schema = response.json()
            status_choices = (
                schema.get("actions", {})
                .get("POST", {})
                .get("status", {})
                .get("choices", [])
            )

            return [choice["value"] for choice in status_choices]

        except requests.exceptions.RequestException as e:
            print(f"Error getting available statuses: {e}")
            return ["active", "staging", "planned", "decommissioning", "retired"]  # Default values


def display_sites(sites, status=None):
    """
    Display sites in readable format

    Args:
        sites (list): List of sites
        status (str): Queried status (for the title)
    """
    if not sites:
        if status:
            print(f"No sites found with status '{status}'")
        else:
            print("No sites found")
        return

    title = f"Sites found"
    if status:
        title += f" with status '{status}'"

    print(f"\n{title} ({len(sites)} sites):")
    print("=" * 60)

    for site in sites:
        print(f"ID: {site.get('id', 'N/A')}")
        print(f"Name: {site.get('name', 'N/A')}")
        print(f"Slug: {site.get('slug', 'N/A')}")
        print(f"Status: {site.get('status', {}).get('label', 'N/A')}")
        print(f"Description: {site.get('description', 'N/A')}")
        print(f"URL: {site.get('url', 'N/A')}")
        print("-" * 40)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Query sites in NetBox by specific status"
    )
    parser.add_argument(
        "--status",
        type=str,
        help="Status of sites to query (active, planned, etc.)",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000",
        help="NetBox base URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--token", type=str, required=True, help="NetBox API token"
    )
    parser.add_argument(
        "--list-statuses", action="store_true", help="Show available statuses"
    )

    args = parser.parse_args()

    # Validate that a status is specified
    if not args.status and not args.list_statuses:
        print("ERROR: You must specify a status with --status or use --list-statuses")
        print("Example: python netbox_sites.py --token your_token --status active")
        sys.exit(1)

    # Create API client
    client = NetBoxAPIClient(args.url, args.token)

    # Show available statuses if requested
    if args.list_statuses:
        print("Available statuses:")
        statuses = client.get_available_statuses()
        for status in statuses:
            print(f"  - {status}")
        return

    # Query sites
    print(f"Querying sites with status '{args.status}' on {args.url}...")
    sites = client.get_sites_by_status(args.status)

    if sites is None:
        print("Error querying the API")
        sys.exit(1)

    # Display results
    display_sites(sites, args.status)


if __name__ == "__main__":
    main()

# Alternative usage example without command line arguments:
"""
# Direct configuration
NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = "your_token_here"

# Create client
client = NetBoxAPIClient(NETBOX_URL, NETBOX_TOKEN)

# Query active sites
sites = client.get_sites_by_status("active")
if sites is not None:
    display_sites(sites, "active")
"""
