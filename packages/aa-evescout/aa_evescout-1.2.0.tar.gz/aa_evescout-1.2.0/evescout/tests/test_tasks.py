import responses

from django.test import TestCase
from eveuniverse.models import EveSolarSystem

from evescout.models import SignatureSystem, Singleton
from evescout.tasks import create_new_signature, update_all_signatures
from evescout.tests.testdata.load_eveuniverse import load_eveuniverse


class TestTasks(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_eveuniverse()

    def test_create_new_signature(self):
        nagamanen = EveSolarSystem.objects.get(id=30002807)

        # Edited signature to match loaded information
        signature_info = {
            "id": "24352",
            "created_at": "2024-11-01T07:21:44.000Z",
            "created_by_id": 2121887172,
            "created_by_name": "Kiera Endymion",
            "updated_at": "2024-11-01T07:26:04.000Z",
            "updated_by_id": 2121887172,
            "updated_by_name": "Kiera Endymion",
            "completed_at": "2024-11-01T07:26:04.000Z",
            "completed_by_id": 2121887172,
            "completed_by_name": "Kiera Endymion",
            "completed": True,
            "wh_exits_outward": False,
            "wh_type": "F135",
            "max_ship_size": "large",
            "expires_at": "2024-11-02T00:21:44.000Z",
            "remaining_hours": 1,
            "signature_type": "wormhole",
            "out_system_id": 31000005,
            "out_system_name": "Thera",
            "out_signature": "GBO-896",
            "in_system_id": 30002807,
            "in_system_class": "ls",
            "in_system_name": "Nagamanen",
            "in_region_id": 10000033,
            "in_region_name": "The Citadel",
            "in_signature": "NNA-392",
        }

        create_new_signature(signature_info)

        signature = SignatureSystem.objects.get(id=24352)

        self.assertEqual(signature.system, nagamanen)
        self.assertEqual(signature.origin, SignatureSystem.SignatureOrigin.THERA)
        self.assertEqual(signature.size, SignatureSystem.WormholeSize.L)

    @responses.activate
    def test_duplicate_signature(self):
        """
        Test that there's no crash or duplicate when an already registered signature is entered
        """
        nagamanen = EveSolarSystem.objects.get(id=30002807)

        SignatureSystem.create(24352, nagamanen, SignatureSystem.SignatureOrigin.THERA)

        # Edited signature to match loaded information
        response_content = [
            {
                "id": "24352",
                "created_at": "2024-11-01T07:21:44.000Z",
                "created_by_id": 2121887172,
                "created_by_name": "Kiera Endymion",
                "updated_at": "2024-11-01T07:26:04.000Z",
                "updated_by_id": 2121887172,
                "updated_by_name": "Kiera Endymion",
                "completed_at": "2024-11-01T07:26:04.000Z",
                "completed_by_id": 2121887172,
                "completed_by_name": "Kiera Endymion",
                "completed": True,
                "wh_exits_outward": False,
                "wh_type": "F135",
                "max_ship_size": "large",
                "expires_at": "2024-11-02T00:21:44.000Z",
                "remaining_hours": 1,
                "signature_type": "wormhole",
                "out_system_id": 31000005,
                "out_system_name": "Thera",
                "out_signature": "GBO-896",
                "in_system_id": 30002807,
                "in_system_class": "ls",
                "in_system_name": "Nagamanen",
                "in_region_id": 10000033,
                "in_region_name": "The Citadel",
                "in_signature": "NNA-392",
            }
        ]

        responses.get(
            "https://api.eve-scout.com/v2/public/signatures", json=response_content
        )

        update_all_signatures()

        self.assertEqual(1, SignatureSystem.objects.count())

    @responses.activate
    def test_delete_signature(self):
        # Imaginary signature with non existing id
        SignatureSystem.create(
            00, EveSolarSystem.objects.all()[0], SignatureSystem.SignatureOrigin.THERA
        )

        response_content = []

        responses.get(
            "https://api.eve-scout.com/v2/public/signatures", json=response_content
        )

        update_all_signatures()

        self.assertEqual(0, SignatureSystem.objects.count())

    @responses.activate
    def test_no_update_if_after_check(self):
        """
        Checks that the database isn't altered if the last_check flag is bigger than the header value
        """

        # Edited signature to match loaded information
        response_content = [
            {
                "id": "24352",
                "created_at": "2024-11-01T07:21:44.000Z",
                "created_by_id": 2121887172,
                "created_by_name": "Kiera Endymion",
                "updated_at": "2024-11-01T07:26:04.000Z",
                "updated_by_id": 2121887172,
                "updated_by_name": "Kiera Endymion",
                "completed_at": "2024-11-01T07:26:04.000Z",
                "completed_by_id": 2121887172,
                "completed_by_name": "Kiera Endymion",
                "completed": True,
                "wh_exits_outward": False,
                "wh_type": "F135",
                "max_ship_size": "large",
                "expires_at": "2024-11-02T00:21:44.000Z",
                "remaining_hours": 1,
                "signature_type": "wormhole",
                "out_system_id": 31000005,
                "out_system_name": "Thera",
                "out_signature": "GBO-896",
                "in_system_id": 30002807,
                "in_system_class": "ls",
                "in_system_name": "Nagamanen",
                "in_region_id": 10000033,
                "in_region_name": "The Citadel",
                "in_signature": "NNA-392",
            }
        ]

        response_header = {
            "x-last-signaleer-hub-interaction": "2004-11-08T15:13:09.052Z",  # value well in the past
        }

        responses.get(
            "https://api.eve-scout.com/v2/public/signatures",
            json=response_content,
            headers=response_header,
        )

        Singleton.update_check_time()

        update_all_signatures()

        self.assertEqual(0, SignatureSystem.objects.count())

        update_all_signatures(ignore_last_check=True)

        self.assertEqual(1, SignatureSystem.objects.count())
