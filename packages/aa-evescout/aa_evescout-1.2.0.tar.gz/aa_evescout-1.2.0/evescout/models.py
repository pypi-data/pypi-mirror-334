"""Models."""

import sys
from collections.abc import Iterable

from aadiscordbot.tasks import send_message
from discord import Color
from solo.models import SingletonModel

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from eveuniverse.helpers import meters_to_ly
from eveuniverse.models import EveSolarSystem

from allianceauth.services.hooks import get_extension_logger

from .utils import default_embed

logger = get_extension_logger(__name__)


class General(models.Model):
    """A meta model for app permissions."""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (("create_pinger", "Can create a pinger in a discord channel"),)


class Singleton(SingletonModel):
    """Singleton preserving information on the previous requests"""

    last_check = models.DateTimeField(
        default=timezone.now,
        help_text="Stores the last time we had new API data to work with",
    )

    @classmethod
    def get_last_check_time(cls):
        """Get the last time signatures were checked"""
        return cls.get_solo().last_check

    @classmethod
    def update_check_time(cls):
        """Update `last_check` to now after updating data correctly"""
        singleton = cls.get_solo()
        singleton.last_check = timezone.now()
        singleton.save()

    def __str__(self):
        return "Evescout Signleton"


class SignaturePinger(models.Model):
    """System to be watched and ping if a signature appear close to this system"""

    class PingType(models.TextChoices):
        """Ways to ping on discord"""

        NONE = " ", "None"
        HERE = "@here", "@here"
        EVERYONE = "@everyone", "@everyone"

    system = models.ForeignKey(
        EveSolarSystem,
        null=True,
        on_delete=models.CASCADE,
        help_text="System to be watched",
    )
    discord_channel_id = models.BigIntegerField(help_text="Discord channel id to ping")

    ping_for_thera = models.BooleanField(
        default=True, help_text="If there should be a ping for Thera connections"
    )
    ping_for_turnur = models.BooleanField(
        default=True, help_text="If there should be a ping for Turnur connections"
    )

    ping_type = models.CharField(
        max_length=9,
        choices=PingType.choices,
        default=PingType.NONE,
        help_text="Type of notification that should be sent out with the ping",
    )

    always_ping = models.BooleanField(
        default=False,
        help_text="Will bypass the minimum distances and always ping when a new signature is detected."
        "System selection still applies",
    )

    min_ping_distance_ly = models.FloatField(
        default=0,
        help_text="Ping if the signature spawns less than this amount of light years",
        validators=[
            MinValueValidator(0),
        ],
    )
    min_ping_distance_jump = models.IntegerField(
        default=0,
        help_text="ping if the signature spawns less than this amount of jumps",
        validators=[
            MinValueValidator(0),
        ],
    )

    ping_here_under_distance_ly = models.FloatField(
        blank=True,
        null=True,
        help_text="Will overwrite the default ping type and send a @here under this distance in light years",
    )
    ping_here_under_distance_jump = models.IntegerField(
        blank=True,
        null=True,
        help_text="Will overwrite the default ping type and send a @here under this distance in gate jumps",
    )

    ping_everyone_under_distance_ly = models.FloatField(
        blank=True,
        null=True,
        help_text="Will overwrite the default ping type and send a @everyone under this distance in light years",
    )
    ping_everyone_under_distance_jump = models.IntegerField(
        blank=True,
        null=True,
        help_text="Will overwrite the default ping type and send a @everyone under this distance in gate jumps",
    )

    @classmethod
    def create(
        cls, discord_channel_id: int, solar_system: EveSolarSystem | None = None
    ) -> "SignaturePinger":
        """Instantiate new pinger"""
        return cls.objects.create(
            discord_channel_id=discord_channel_id, system=solar_system
        )

    def get_ping_type_for_range(self, jumps: int, light_years: float) -> str:
        """
        Return what kind of ping should be sent out for a signature at the given range
        """
        logger.debug(
            "Checking ping type for pinger id %d with jump %d and light_years %d",
            self.id,
            jumps,
            light_years,
        )
        if (
            self.ping_everyone_under_distance_ly
            and self.ping_everyone_under_distance_ly >= light_years
        ) or (
            self.ping_everyone_under_distance_jump
            and self.ping_everyone_under_distance_jump >= jumps
        ):
            logger.debug("Returning everyone")
            return self.PingType.EVERYONE.value
        if (
            self.ping_here_under_distance_ly
            and self.ping_here_under_distance_ly >= light_years
        ) or (
            self.ping_here_under_distance_jump
            and self.ping_here_under_distance_jump >= jumps
        ):
            logger.debug("Returning here")
            return self.PingType.HERE.value

        logger.debug("Returning default: '%s'", self.ping_type)
        return self.ping_type

    def ping_new_sig(self, signature: "SignatureSystem"):
        """Sends a message on discord to warn for a new signature"""
        gate_jumps, light_years = signature.distance_from_pinger(self)
        e = default_embed(
            f"New signature from {signature.origin_system_name()} detected in {signature.system.name}"
        )
        e.add_field(
            name=f"Distance from {self.system.name}",
            value=f"{gate_jumps} jumps / {round(light_years, 2)} ly.",
        )
        e.add_field(
            name="Wormhole size",
            value=SignatureSystem.WormholeSize.from_value_to_label(signature.size),
        )

        if signature.system.is_high_sec:
            e.color = Color.blue()
        elif signature.system.is_low_sec:
            e.color = Color.yellow()
        elif signature.system.is_null_sec:
            e.color = Color.purple()

        send_message(
            channel_id=self.discord_channel_id,
            embed=e,
            message=self.get_ping_type_for_range(gate_jumps, light_years),
        )

    def __str__(self):
        if system := self.system:
            return f"Pinger {system.name}"
        return f"Unlinked pinger {self.id}"


class SignatureSystem(models.Model):
    """Represents a system in which a sig was detected"""

    class SignatureOrigin(models.TextChoices):
        """Possible origins of a wormhole"""

        THERA = "TH", "Thera"
        TURNUR = "TU", "Turnur"

    class WormholeSize(models.TextChoices):
        """Possible size of the wormhole"""

        C = "C", "Capital"
        XL = "XL", "Extra-Large"
        L = "L", "Large"
        M = "M", "Medium"
        S = "S", "Small"

        @classmethod
        def from_value_to_label(cls, value: str | None) -> str:
            """Return the label from one of the possible values"""
            if value is None:
                return "Unknown"
            return getattr(cls, value).label

    id = models.IntegerField(primary_key=True, help_text="Eve scout signature id")

    system = models.ForeignKey(
        EveSolarSystem,
        on_delete=models.CASCADE,
        help_text="System in which the signature appeared",
    )
    origin = models.CharField(
        max_length=2,
        choices=SignatureOrigin.choices,
        help_text="Where the signature originates from",
    )
    size = models.CharField(
        max_length=2,
        null=True,
        choices=WormholeSize.choices,
        help_text="Size of the wormhole",
    )

    @classmethod
    def create(
        cls,
        signature_id: int,
        system: EveSolarSystem,
        origin: SignatureOrigin,
        size: WormholeSize | None = None,
    ) -> "SignatureSystem":
        """Creates a new signature"""
        logger.debug(
            "Creating a signature of size %s in %s from %s with id %s",
            size,
            system,
            origin,
            signature_id,
        )
        return cls.objects.create(
            id=signature_id, system=system, origin=origin, size=size
        )

    @classmethod
    def get_signatures_from(cls, system: SignatureOrigin) -> list["SignatureSystem"]:
        """Returns all signatures linked to a system"""
        return cls.objects.filter(origin=system)

    @classmethod
    def get_signature_ids_set(cls) -> set[int]:
        """Return a set with the signature id of all signatures in the database"""
        id_list = cls.objects.values_list("id", flat=True)
        return set(id_list)

    @classmethod
    def delete_disappeared_signatures(cls, existing_signatures_ids: Iterable[int]):
        """Gets a list of signature ids. Will delete all Signatures that are not part of this list"""

        disappeared_signatures = cls.objects.exclude(id__in=existing_signatures_ids)
        disappeared_signatures.delete()

        logger.debug("Deleted % signature(s)", disappeared_signatures.count())

    @classmethod
    def get_closest_signature(
        cls, solar_system: EveSolarSystem, origin: SignatureOrigin
    ) -> list["SignatureSystem"]:
        """
        Will return the closes signature linked to `origin` from `solar_system`
        Return is made as a list to be able to return several systems if they are at similar ranges
        """
        best_range = sys.maxsize
        best_systems = []
        for signature_system in cls.get_signatures_from(origin):
            distance_gates, _ = signature_system.distance_from_solar_system(
                solar_system
            )
            if distance_gates < best_range:
                best_range = distance_gates
                best_systems = [signature_system]
            elif distance_gates == best_range:
                best_systems.append(signature_system)

        return best_systems

    def origin_system_name(self) -> str:
        """Returns the human-readable origin system"""
        match self.origin:
            case self.SignatureOrigin.THERA:
                return "Thera"
            case self.SignatureOrigin.TURNUR:
                return "Turnur"

    def distance_from_solar_system(self, solar_system: EveSolarSystem) -> (int, float):
        """
        Return the distance from the signature and a solar system in gate jumps and light years
        """
        if route := solar_system.route_to(self.system):
            gate_jumps = len(route) - 1  # -1 to avoid counting the initial system
            light_years = meters_to_ly(solar_system.distance_to(self.system))
            return gate_jumps, light_years

        return sys.maxsize, float("inf")

    def distance_from_pinger(self, pinger: SignaturePinger) -> (int, float):
        """
        Return the distance from the pinger system in gate jumps and light years
        """
        if pinger_system := pinger.system:
            return self.distance_from_solar_system(pinger_system)
        return sys.maxsize, float("inf")

    def is_pinger_in_range(self, pinger: SignaturePinger) -> bool:
        """True if the pinger is in rage for gates or jump range"""
        if self.system.is_trig_space or self.system.is_w_space:
            return False

        if pinger.always_ping:
            return True

        gate_jumps, light_years = self.distance_from_pinger(pinger)
        return (
            gate_jumps <= pinger.min_ping_distance_jump
            or light_years <= pinger.min_ping_distance_ly
        )

    def pingers_in_range(self) -> list[SignaturePinger]:
        """Returns all pingers with their get/distance parameters near the signature"""
        return [
            pinger
            for pinger in SignaturePinger.objects.all()
            if self.is_pinger_in_range(pinger)
        ]

    def get_size_str(self) -> str:
        """Get a readable size"""
        return SignatureSystem.WormholeSize.from_value_to_label(self.size)

    def __str__(self):
        return f"Signature {self.origin} > {self.system}"
