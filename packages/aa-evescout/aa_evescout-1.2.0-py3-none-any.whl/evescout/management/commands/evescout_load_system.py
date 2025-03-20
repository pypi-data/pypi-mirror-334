"""Load a missing system"""

from django.core.management import BaseCommand
from eveuniverse.models import EveSolarSystem

from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


class Command(BaseCommand):
    help = "Loads a system missing from eveuniverse"

    def add_arguments(self, parser):
        parser.add_argument("solar_system_id", type=int)

    def handle(self, *args, **options):
        solar_system_id = options["solar_system_id"]
        logger.info("Loading system %s", solar_system_id)

        EveSolarSystem.objects.update_or_create_esi(id=solar_system_id)
