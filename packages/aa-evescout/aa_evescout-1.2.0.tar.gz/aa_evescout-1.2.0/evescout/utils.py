"""Global utility functions for the module"""

from discord import Embed

from esi.clients import EsiClientProvider
from eveuniverse.models import EveSolarSystem

from allianceauth.services.hooks import get_extension_logger

from . import __version__

logger = get_extension_logger(__name__)

esi = EsiClientProvider(app_info_text=f"aa-evescout v{__version__}")


def default_embed(title: str) -> Embed:
    """Returns the default embed layout to use accross the app"""
    e = Embed(
        title=title,
    )
    e.set_author(
        name="EVE-scout",
        url="https://eve-scout.com/#/",
        icon_url="https://images.evetech.net/alliances/99005130/logo?size=128",
    )

    return e


# pylint: disable=inconsistent-return-statements
def find_solar_system_from_str(solar_system_name: str) -> EveSolarSystem | None:
    """
    Will attempt to load a system from it's string
    """
    logger.debug("Trying to find solar system for name %s", solar_system_name)
    try:
        solar_system = EveSolarSystem.objects.get(name=solar_system_name)
        return solar_system
    except EveSolarSystem.DoesNotExist:
        logger.debug(
            "Couldn't find %s in database, trying to find the id from esi",
            solar_system_name,
        )
        solar_system_id_result = esi.client.Universe.post_universe_ids(
            names=[solar_system_name]
        ).result()
        if id_list := solar_system_id_result["systems"]:
            solar_system_id = id_list[0]["id"]
            solar_system, _ = EveSolarSystem.objects.get_or_create_esi(
                id=solar_system_id
            )
            logger.info(
                "Created system id %s matching name %s",
                solar_system.id,
                solar_system_name,
            )
            return solar_system

    logger.error("Couldn't find a matching id for %s", solar_system_name)
    return
