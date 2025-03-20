from django.test import TestCase
from eveuniverse.models import EveSolarSystem

from evescout.models import SignatureSystem
from evescout.tests.testdata.load_eveuniverse import load_eveuniverse


class TestSignatures(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_eveuniverse()

    def test_get_ids_set(self):
        oto = EveSolarSystem.objects.get(id=30002808)

        SignatureSystem.objects.create(
            id=1, system=oto, origin=SignatureSystem.SignatureOrigin.THERA
        )
        SignatureSystem.objects.create(
            id=2, system=oto, origin=SignatureSystem.SignatureOrigin.THERA
        )

        ids_set = SignatureSystem.get_signature_ids_set()

        self.assertEqual({1, 2}, ids_set)

    def test_disappeared_signatures(self):
        oto = EveSolarSystem.objects.get(id=30002808)

        sig_system_1 = SignatureSystem.objects.create(
            id=1, system=oto, origin=SignatureSystem.SignatureOrigin.THERA
        )
        sig_system_2 = SignatureSystem.objects.create(
            id=2, system=oto, origin=SignatureSystem.SignatureOrigin.THERA
        )

        SignatureSystem.delete_disappeared_signatures([1])

        self.assertEqual(1, SignatureSystem.objects.count())
        self.assertIn(sig_system_1, SignatureSystem.objects.all())
        self.assertNotIn(sig_system_2, SignatureSystem.objects.all())

    def test_get_closest_signatures(self):
        oto = EveSolarSystem.objects.get(name="Oto")
        sujarento = EveSolarSystem.objects.get(name="Sujarento")
        hasmijaala = EveSolarSystem.objects.get(name="Hasmijaala")
        nagamanen = EveSolarSystem.objects.get(name="Nagamanen")

        sig_system_1 = SignatureSystem.objects.create(
            id=1,
            system=sujarento,
            origin=SignatureSystem.SignatureOrigin.THERA,
        )
        sig_system_2 = SignatureSystem.objects.create(
            id=2,
            system=hasmijaala,
            origin=SignatureSystem.SignatureOrigin.THERA,
        )

        thera_output = SignatureSystem.get_closest_signature(
            oto, SignatureSystem.SignatureOrigin.THERA
        )
        self.assertEqual(2, len(thera_output))
        self.assertIn(sig_system_1, thera_output)
        self.assertIn(sig_system_2, thera_output)

        empty_output = SignatureSystem.get_closest_signature(
            oto, SignatureSystem.SignatureOrigin.TURNUR
        )
        self.assertEqual(0, len(empty_output))

        sig_system_3 = SignatureSystem.objects.create(
            id=3, system=nagamanen, origin=SignatureSystem.SignatureOrigin.TURNUR
        )

        turnur_ouput = SignatureSystem.get_closest_signature(
            oto, SignatureSystem.SignatureOrigin.TURNUR
        )
        self.assertEqual(1, len(turnur_ouput))
        self.assertIn(sig_system_3, turnur_ouput)

        thera_output = SignatureSystem.get_closest_signature(
            oto, SignatureSystem.SignatureOrigin.THERA
        )
        self.assertEqual(2, len(thera_output))
        self.assertIn(sig_system_1, thera_output)
        self.assertIn(sig_system_2, thera_output)
        self.assertNotIn(sig_system_3, thera_output)

    def test_unknown_size_signature(self):
        oto = EveSolarSystem.objects.get(name="Oto")

        sig_system = SignatureSystem.objects.create(
            id=1,
            system=oto,
            origin=SignatureSystem.SignatureOrigin.THERA,
        )

        self.assertIsNone(sig_system.size)

        self.assertEqual(
            "Unknown", SignatureSystem.WormholeSize.from_value_to_label(sig_system.size)
        )
