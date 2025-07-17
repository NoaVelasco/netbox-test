# NetBox tasks

## Installing NetBox
This repository includes the official NetBox Docker repository (v3.3.0) customized, so clone this:

```
$ git clone ...
$ cd netbox-docker

$ docker compose pull
$ docker compose up

```

If the superuser variables doesn't set it up automatically, we create a superuser to enter the application:

```
$ docker compose exec netbox /opt/netbox/netbox/manage.py createsuperuser
```

## Adding data
Add new sites through the NetBox UI. Go to Organization/Sites and click Import. 

![adding data](how-to/add-data.jpg)

Upload the file [initial_data.yaml](initial_data.yaml).

## Adding scripts
In NetBox UI, go to Customization/Scripts and clic Add.

![adding scripts](how-to/add-scripts.jpg)

Upload the files [SiteFilter.py](scripts/SiteFilter.py) and QuerySitesCount.py.