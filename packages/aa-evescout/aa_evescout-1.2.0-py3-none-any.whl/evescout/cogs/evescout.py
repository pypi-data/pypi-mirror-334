from aadiscordbot.app_settings import get_site_url
from aadiscordbot.cogs.utils.decorators import sender_has_perm
from discord import ApplicationContext, SlashCommandGroup, option
from discord.ext import commands

from django.conf import settings
from eveuniverse.models import EveSolarSystem

from allianceauth.services.hooks import get_extension_logger

from evescout.cogs.utils.autocompletes import possible_regions
from evescout.cogs.utils.region_obs import REGION_OBS
from evescout.models import SignaturePinger, SignatureSystem
from evescout.utils import default_embed, find_solar_system_from_str

from ..evescout import routes_jove_observatories
from .utils.autocompletes import possible_origins, search_solar_system

logger = get_extension_logger(__name__)


def _signature_info(signature: SignatureSystem, solar_system: EveSolarSystem) -> str:
    """Return the signature info to be put in an embed field value"""
    gates, light_years = signature.distance_from_solar_system(solar_system)
    return (
        f"Distance:\n"
        f"- {gates} gates\n"
        f"- {round(light_years, 2)} ly.\n"
        f"Size: {signature.get_size_str()}\n"
    )


class EveScout(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    evescout_commands = SlashCommandGroup(
        "evescout", "EVE-Scouts", guild_ids=[int(settings.DISCORD_GUILD_ID)]
    )

    @evescout_commands.command(
        name="initiate-pinger",
        description="Initiate the configuration for pings when a Thera/Turnur connection is reported",
    )
    @sender_has_perm("evescout.create_pinger")
    async def initiate_pinger(self, ctx: ApplicationContext):
        """Creates a new pinger and link it to the channel the command was called in"""
        channel_id = ctx.channel_id
        logger.info("Creating a pinger for channel id %s", channel_id)

        pinger = SignaturePinger.create(channel_id)

        site_url = get_site_url()
        pinger_url = f"{site_url}/admin/evescout/signaturepinger/{pinger.id}"

        return await ctx.respond(
            f"Successfully created a new pinger. You can edit it at {pinger_url}"
        )

    @evescout_commands.command(
        name="closest-signature",
        description="Finds the closest Thera/Turnur connection from the selected system",
    )
    @option(
        "system",
        parameter_name="system_name",
        description="System to search from",
        autocomplete=search_solar_system,
    )
    @option(
        "origin",
        parameter_name="signature_origin_str",
        required=False,
        description="Origin of the closest connection you want (can be empty)",
        autocomplete=possible_origins,
    )
    async def closest_signature(
        self, ctx: ApplicationContext, system_name: str, signature_origin_str: str
    ):
        logger.debug(
            "Received a closest_signature command with arguments %s, %s",
            system_name,
            signature_origin_str,
        )

        await ctx.defer()

        solar_system = find_solar_system_from_str(system_name)
        if not solar_system:
            logger.error("Couldn't find a solar system matching name %s", system_name)
            return await ctx.respond(
                f"Couldn't find a solar system matching name `{system_name}`"
            )

        if solar_system.is_w_space:
            logger.error("Won't search connections for wh system %s", solar_system.name)
            return await ctx.respond("Can't search for wh systems")
        elif solar_system.is_trig_space:
            logger.error(
                "Won't search connections for trig system %s", solar_system.name
            )
            return await ctx.respond("Can't search for triglavian systems")

        logger.info(f"Searching connections close to {solar_system.name}")

        e = default_embed(f"Connections close to {solar_system.name}")

        if signature_origin_str in (None, "THERA"):
            for signature in SignatureSystem.get_closest_signature(
                solar_system, SignatureSystem.SignatureOrigin.THERA
            ):
                e.add_field(
                    name=f"Thera connection in {signature.system.name}",
                    value=_signature_info(signature, solar_system),
                )

        if signature_origin_str in (None, "TURNUR"):
            for signature in SignatureSystem.get_closest_signature(
                solar_system, SignatureSystem.SignatureOrigin.TURNUR
            ):
                e.add_field(
                    name=f"Turnur connection in {signature.system.name}",
                    value=_signature_info(signature, solar_system),
                )

        await ctx.respond(embed=e)

    @evescout_commands.command(
        name="drifters", description="List drifter observatories arround a system"
    )
    @option(
        "system",
        parameter_name="system_name",
        description="System to search from",
        autocomplete=search_solar_system,
    )
    async def drifter_orbservatories(self, ctx: ApplicationContext, system_name: str):
        logger.info("Returning drifter wormholes around %s", system_name)
        await ctx.defer()

        solar_system = find_solar_system_from_str(system_name)

        routes = routes_jove_observatories(solar_system)

        e = default_embed(f"Jove observatories around {solar_system.name}")

        for system in routes:
            e.add_field(name=system["to"], value=f"{system['jumps']} jumps out")

        return await ctx.respond(embed=e)

    @evescout_commands.command(
        name="region-observatories",
        description="Returns the dotlan region URL with all observatory systems selected",
    )
    @option(
        "region-name",
        parameter_name="region_name",
        description="Name of the region to return",
        autocomplete=possible_regions,
    )
    async def region_observatories(self, ctx: ApplicationContext, region_name: str):
        logger.info("Trying to return the observatories in the region %s", region_name)

        try:
            embed_title = f"Jove observatories in {region_name}"
        except KeyError:
            embed_title = f"{region_name} is not a valid region name"

        e = default_embed(embed_title)
        e.add_field(name="dotlan", value=REGION_OBS[region_name])
        e.set_footer(text="The data isn't perfect. Please repport any mistake.")

        return await ctx.respond(embed=e)


def setup(bot):
    bot.add_cog(EveScout(bot))
