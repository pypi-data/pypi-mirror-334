from django.core.management import BaseCommand

from allianceauth.services.hooks import get_extension_logger

from evescout.tasks import update_all_signatures

logger = get_extension_logger(__name__)


class Command(BaseCommand):
    help = "Updates all signatures from the eve-scout API"

    def handle(self, *args, **options):
        logger.info("Updating signatures from command line")
        update_all_signatures.delay(ignore_last_check=True)
