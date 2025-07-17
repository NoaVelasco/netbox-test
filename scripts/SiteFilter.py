from extras.scripts import *
from dcim.models import Site
from django.utils.text import slugify
import yaml


class SiteFilter(Script):
    """
    Script to filter sites based on a specific state: active or planned.
    """

    class Meta:
        name = "Site Filter Report"
        description = (
            "Filter sites based on a specific state and return them in YAML format."
        )

    # Field to select the site status
    status = ChoiceVar(
        description="Site Status",
        required=True,
        choices=[("active", "Active"), ("planned", "Planned")],
    )

    def run(self, data, commit):

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
        return yaml.dump(output_data)
