# NetBox tasks

## Installing NetBox

Clone this repository:

```bash
git clone https://github.com/NoaVelasco/netbox-test.git
cd netbox-test
```

This repository includes a customized NetBox Docker repository (v3.3.0) as a submodule. If it can't be accessed, follow these steps.

1. Clone the original NetBox-Docker repository in `netbox-test`:

```bash
git clone https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
```
2. Copy the [docker-compose.override.yml](docker-compose.override.yml) file of **this** repository into this directory or create it: 
```bash
echo 'services:
  netbox:
    ports:
      - "8000:8080"' > docker-compose.override.yml

# You can add environment variables:
    # environment:
      # SKIP_SUPERUSER: "false"
      # SUPERUSER_API_TOKEN: ""
      # SUPERUSER_EMAIL: ""
      # SUPERUSER_NAME: ""
      # SUPERUSER_PASSWORD: ""
```


Run Docker:
```bash
docker compose pull
docker compose up
```

The superuser environment variables are not included because it is not safe to share them in public repositories (and Github will send warning messages). You must create a superuser to access the application:

```bash
docker compose exec netbox /opt/netbox/netbox/manage.py createsuperuser

# Then it'll ask for a username, an email and a password.
```


## Adding data
Add new sites through the NetBox UI. Go to Organization/Sites and click Import. 

![adding data](how-to/add-data.jpg)

Upload the file [initial_data.yaml](initial_data.yaml).

## Adding custom script
In NetBox UI, go to Customization/Scripts and click Add.

![adding scripts](how-to/add-scripts.jpg)

Upload the file [SiteFilter.py](scripts/SiteFilter.py) located in the `custom_scripts` directory.

To run the script, just click on the name. The result will be like this:

![api-token](how-to/custom-script-output.jpg)


## Running API script
This script allows you to query NetBox sites by their status using the API. It's in the root directory of the repository: [netbox_sites.py](netbox_sites.py).

It's recommended to set up a virtual environment, but in most scenarios it would be unnecessary.  

```bash
cd netbox-test
python3 -m venv .venv

source .venv/bin/activate
# probably you already have the requests library. If not:
pip install requests

# or just install requirements
pip install -r requirements.txt
```

**Options**. You can ask for help with `python3 netbox_sites.py --help`:
```
usage: netbox_sites.py [-h] [--status STATUS] [--url URL] --token TOKEN [--list-statuses]

Query sites in NetBox by specific status

options:
  -h, --help       show this help message and exit

  # The script waits for the next arguments:
  --status STATUS  Status of sites to query (active, planned, etc.)
  --url URL        NetBox base URL (default: http://localhost:8000)
  --token TOKEN    NetBox API token
  --list-statuses  Show available statuses
```

To run the script, you need the API token and the status. If you don't provide a URL, the script uses http://localhost:8000 by default.  

You can create a new token through the user menu:

![api-token](how-to/api-token.jpg)

In this case, you can simply write:

```bash
python3 netbox_sites.py --token "<YOUR_API_TOKEN>" --status planned
```

and get this output: 

```
Querying sites with status 'planned' on http://localhost:8000...

Sites found with status 'planned' (2 sites):
============================================================
ID: 5
Name: Site 1
Slug: site_1
Status: Planned
Description:
URL: http://localhost:8000/api/dcim/sites/5/
----------------------------------------
ID: 6
Name: Site 2
Slug: site_2
Status: Planned
Description:
URL: http://localhost:8000/api/dcim/sites/6/
----------------------------------------
```

## Running Tests

The project includes a comprehensive test suite that uses mock objects to simulate API responses, allowing you to test the functionality without an actual NetBox server connection.

To run the tests:

```bash
# Run all tests
python3 run_tests.py

# Or run a specific test file
python3 -m unittest test_netbox_sites.py
```

The tests cover:
- API client initialization
- Site querying with and without status filters
- Error handling for API requests
- Processing of API responses
- Display formatting of site information


## About my working process
For more info and the steps I followed while working on this test, see [my notes](how-to/notes_en.md).



---

250718 - Noa Velasco