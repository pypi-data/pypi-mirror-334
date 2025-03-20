from django.test import TestCase
from eveuniverse.tools.testdata import ModelSpec, create_testdata

from . import test_data_filename


class CreateEveUniverseTestData(TestCase):
    def test_create_testdata(self):
        test_data_spec = [
            ModelSpec(
                "EveSolarSystem",
                ids=[
                    # Isoma constellation
                    30002806,
                    30002807,
                    30002808,
                    30002809,
                    30002810,
                    30002811,
                    30002812,
                    30002813,
                    # Random wh
                    31001805,
                ],
            ),
        ]
        create_testdata(test_data_spec, test_data_filename())
