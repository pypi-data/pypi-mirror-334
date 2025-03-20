# AA eve-scout

AA module that adds commands to the [allianceauth-discordbot](https://github.com/Solar-Helix-Independent-Transport/allianceauth-discordbot/) related to the [eve-scout](https://eve-scout.com/) API. \
EVE-Scout API documentation can be found [here](https://api.eve-scout.com/ui).

Shoutout to Sky Diamond for the API and EVE-Scout for the tireless scanning.

[![release](https://img.shields.io/pypi/v/aa-evescout?label=release)](https://pypi.org/project/aa-evescout/)
[![python](https://img.shields.io/pypi/pyversions/aa-evescout)](https://pypi.org/project/aa-evescout/)
[![django](https://img.shields.io/pypi/djversions/aa-evescout?label=django)](https://pypi.org/project/aa-evescout/)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/r0kym/aa-evescout/-/blob/master/LICENSE)

## Features
- Automated pings when a connection open in system close to a pre-defined system
- Find connections close to a specific system
- Find drifter observatories close to a specific system

### Screenshots

![example_ping.png](images/example_ping.png)

![example_closest.png](images/example_closest.png)

![example_drifters.png](images/example_drifters.png)

![example_regionobs.png](images/example_regionobs.png)

## Installations

### Step 1 - Check prerequisites

1. aa-evescout is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/auth/allianceauth/) for details)

2. aa-evescout requires two Alliance Auth modules  to function.
   Make sure it is properly setup before going on.
   - [allianceauth-discordbot](https://github.com/Solar-Helix-Independent-Transport/allianceauth-discordbot/)
   - [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse)

### Step 2 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

```bash
pip install aa-evescout
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'evescout'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
CELERYBEAT_SCHEDULE['evescout_update_signatures'] = {
    'task': 'evescout.tasks.update_all_signatures',
    'schedule': crontab(minute='*/6'),
}
```

### Step 4 - Finalize App installation

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

Restart your supervisor services for Auth.

### Step 5 - (OPTIONAL) Load eveuniverse data

**This command isn't mandatory**

If you want to speed up the application in the future you can decide to run
```bash
python manage.py eveuniverse_load_data map
```

This command will take some time to complete and consume a lot of database space.
It isn't mandatory to run it so don't hesitate to skip it if you want to save database space.

## Permissions

Permissions overview.

| Name            | Description                                                                      |
|-----------------|----------------------------------------------------------------------------------|
| `create_pinger` | The user can use the `/evescout initiate-pinger` command in the alliance discord |

## Commands

The following commands can be used when running the module:

| Name                         | Description                                                        |
|------------------------------|--------------------------------------------------------------------|
| `evescout_update_signatures` | Updates all signatures from the EVE-scout API                      |
| `evescout_load_system`       | Manually loads a solar system to the database to use it in pingers |
