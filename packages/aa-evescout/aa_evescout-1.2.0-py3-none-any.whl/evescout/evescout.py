"""
All API calls communicating with https://eve-scout.com/
"""

from datetime import datetime
from enum import Enum

import requests

from eveuniverse.models import EveSolarSystem

from allianceauth.services.hooks import get_extension_logger

from . import __version__, repo_url

BASE_URL = "https://api.eve-scout.com"

logger = get_extension_logger(__name__)


class ScoutedSystems(Enum):
    """
    Enumeration of systems the API is tracking
    In the current state it's only Thera and Turnur
    """

    THERA = "thera"
    TURNUR = "turnur"


class RoutingPreference(Enum):
    """Different ways to route for the pathfinding"""

    SAFER = "safer"
    SHORTEST = "shortest"
    SHORTEST_GATES = "shortest-gates"


class NoUpdatesSinceLastRequest(Exception):
    """Signals that since the last time the API was called data hasn't changed"""


def call_eve_scout_api(url_path: str, query_parameters: dict[str, str] | None = None):
    """Makes the call to the eve-scout API"""
    logger.debug("Querying %s path with %s params", url_path, query_parameters)
    user_agent = f"aa-evescout/{__version__} (+{repo_url})"
    r = requests.get(
        f"{BASE_URL}/{url_path}",
        params=query_parameters,
        headers={"User-Agent": user_agent},
        timeout=10,
    )
    logger.debug("%s returned a code %s", url_path, r.status_code)
    r.raise_for_status()

    return r.json(), r.headers


def list_public_signatures(last_check: datetime | None = None) -> list[dict]:
    """
    Calls the /v2/public/signatures
    Doc: https://api.eve-scout.com/ui/#get-/v2/public/signatures

    Note: here a check of the endpoint headers will be performed.
    An error returned if there has been no modifications since `last_check` was called.
    """
    logger.info("Requesting all sigs from the API")

    response = call_eve_scout_api("v2/public/signatures")

    if last_check and response[1].get("x-last-signaleer-hub-interaction"):
        # last_update = datetime.fromisoformat(
        #     response[1]["X-Last-Signaleer-Hub-Interaction"][:-5] + "Z"
        # )
        last_update = datetime.strptime(
            response[1]["x-last-signaleer-hub-interaction"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        if last_check > last_update:
            logger.info("No updates in the backend since our last successful update")
            raise NoUpdatesSinceLastRequest

    logger.debug("Successfully retrieved data from EVE-scout %s", response)
    return response[0]


def routes_signatures(
    from_system: EveSolarSystem,
    system_name: ScoutedSystems,
    preference: RoutingPreference = RoutingPreference.SAFER,
) -> list[dict]:
    """
    Calls the /v2/public/routes/signatures endpoint
    Doc: https://api.eve-scout.com/ui/#get-/v2/public/routes/signatures
    """
    logger.info(
        "Requesting eve-scout routes from %s to %s with pref %s",
        from_system,
        system_name,
        preference,
    )

    return call_eve_scout_api(
        "v2/public/routes/signatures",
        {
            "from": from_system.name,
            "system_name": system_name.value,
            "preference": preference.value,
        },
    )[0]


def routes_jove_observatories(
    from_system: EveSolarSystem, preference: RoutingPreference = RoutingPreference.SAFER
) -> list[dict]:
    """
    Calls the /v2/public/routes/joveobservatories endpoint
    Doc: https://api.eve-scout.com/ui/#get-/v2/public/routes/joveobservatories
    """
    logger.info(
        "Requesting jove observatories around %s with preference %s",
        from_system,
        preference,
    )

    return call_eve_scout_api(
        "v2/public/routes/joveobservatories",
        {
            "from": from_system.name,
            "preference": preference.value,
        },
    )[0]
