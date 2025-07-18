"""
Site Filter Report Script for NetBox UI

This custom script allows users to filter NetBox sites based on their status (active or planned)
and generates a standardized report in YAML format.
"""

from extras.scripts import Script, ChoiceVar
from dcim.models import Site
from django.utils.text import slugify
import yaml


class SiteFilter(Script):
    """
    A NetBox custom script that filters sites based on their status (active or planned).
    
    This script:
    1. Create a required status filter
    2. Query the NetBox database for matching sites
    3. Generate standardized log entries for each site
    4. Output results in YAML format
    """

    class Meta:
        """
        Metadata for the script that appears in the NetBox UI.
        """
        name = "Site Status Filter Report"
        description = (
            "Filter sites by status (active or planned) and generate YAML output."
        )

    # Field to select the site status
    status = ChoiceVar(
        description="Select the site status to filter",
        required=True,
        choices=[("active", "Active"), ("planned", "Planned")],
    )

    def run(self, data, commit):
        """
        Execute the script to filter sites by status and generate YAML output.
        
        Args:
            data (dict): Contains form data submitted by the user, including the selected status
            commit (bool): Indicates whether database changes should be committed
                          (not used in this read-only script)
        
        Returns:
            str: YAML-formatted string containing the filtered site information
        """
        selected_statuses = data["status"]

        # Filter sites based on the selected status
        sites = Site.objects.filter(status=slugify(selected_statuses))

        # iterate through all sites that match the selected filter criteria
        for site in sites:
            # Log in required format
            # If we don't scape hashtag, it will be interpreted as a header mark
            self.log_info(f"\#{site.id}: {site.name} - {site.status}")

        # Output in YAML format
        output_data = [
            {"id": site.id, "name": site.name, "status": site.status} for site in sites
        ]

        # If no sites found, return a message
        if not output_data:
            self.log_warning("No sites found with the selected status.")
            return "No sites found."
        return yaml.dump(output_data)
