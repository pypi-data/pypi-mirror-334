"""Tasks."""

from celery import shared_task

from eveuniverse.models import EveSolarSystem

from allianceauth.services.hooks import get_extension_logger

from evescout.evescout import NoUpdatesSinceLastRequest, list_public_signatures
from evescout.models import SignatureSystem, Singleton

logger = get_extension_logger(__name__)


@shared_task
def update_all_signatures(*, ignore_last_check: bool = False):
    """
    Update all SignatureSystems from the results of a call to eve-scout

    ignore_last_check param set to true will ignore the update flag of the request.
    Data will be updated even if the auth has the most up-to-date version
    """
    logger.info("Updating all signatures from eve-scout task started")

    if ignore_last_check:
        last_check = None
        logger.debug("Ignoring last_check setting")
    else:
        last_check = Singleton.get_last_check_time()
        logger.debug("Last check setting is at %s", last_check)

    try:
        public_signatures = list_public_signatures(last_check)
    except NoUpdatesSinceLastRequest:
        logger.info("No new update on the EVE-scout API. Terminating")
        return

    existing_ids = {signature["id"] for signature in public_signatures}
    SignatureSystem.delete_disappeared_signatures(existing_ids)

    signatures_in_database = SignatureSystem.get_signature_ids_set()

    for signature_info in public_signatures:
        if int(signature_info["id"]) not in signatures_in_database:
            create_new_signature.delay(signature_info)

    Singleton.update_check_time()


@shared_task
def create_new_signature(signature_info: dict):
    """
    Creates a new signature from the information eve scout gives
    """

    logger.debug("Creating a signature from %s", signature_info)

    match signature_info["out_system_name"]:
        case "Thera":
            signature_origin = SignatureSystem.SignatureOrigin.THERA
        case "Turnur":
            signature_origin = SignatureSystem.SignatureOrigin.TURNUR
        case _:
            raise ValueError(
                f"Unexpected out_system_name value received {signature_info['out_system_name']}"
            )

    match signature_info["max_ship_size"]:
        case "small":
            wormhole_size = SignatureSystem.WormholeSize.S
        case "medium":
            wormhole_size = SignatureSystem.WormholeSize.M
        case "large":
            wormhole_size = SignatureSystem.WormholeSize.L
        case "xlarge":
            wormhole_size = SignatureSystem.WormholeSize.XL
        case "capital":
            wormhole_size = SignatureSystem.WormholeSize.C
        case "unknown" | _:
            wormhole_size = None

    solar_system, _ = EveSolarSystem.objects.get_or_create_esi(
        id=signature_info["in_system_id"]
    )

    signature_system = SignatureSystem.create(
        signature_info["id"], solar_system, signature_origin, wormhole_size
    )

    for pinger in signature_system.pingers_in_range():
        logger.info(
            "Sending ping for sig id %s to pinger id %s", signature_system.id, pinger.id
        )
        pinger.ping_new_sig(signature_system)
