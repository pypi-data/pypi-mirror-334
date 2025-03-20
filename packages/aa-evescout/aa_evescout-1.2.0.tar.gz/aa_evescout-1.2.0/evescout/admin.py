"""Admin site."""

from aadiscordbot.tasks import send_message

from django.contrib import admin

from evescout.models import SignaturePinger, SignatureSystem
from evescout.utils import default_embed


@admin.action(description="Send a test ping")
def send_test_ping(modeladmin, request, queryset):
    """Sends a test ping to all selected pingers"""
    for pinger in queryset:
        e = default_embed("Test ping")
        e.add_field(name="Test ping sent by aa-evescout", value="")
        send_message(channel_id=pinger.discord_channel_id, embed=e)


@admin.register(SignaturePinger)
class SignaturePingerAdmin(admin.ModelAdmin):
    list_display = [
        "system",
        "discord_channel_id",
        "ping_for_thera",
        "ping_for_turnur",
        "ping_type",
        "min_ping_distance_ly",
        "min_ping_distance_jump",
    ]
    actions = [send_test_ping]
    fields = [
        ("system"),
        ("discord_channel_id"),
        ("always_ping"),
        ("ping_for_thera", "ping_for_turnur"),
        ("ping_type"),
        ("min_ping_distance_ly", "min_ping_distance_jump"),
        ("ping_here_under_distance_ly", "ping_here_under_distance_jump"),
        ("ping_everyone_under_distance_ly", "ping_everyone_under_distance_jump"),
    ]


@admin.register(SignatureSystem)
class SignatureSystemAdmin(admin.ModelAdmin):
    list_display = ["system", "origin", "size"]
    list_filter = ["origin", "size"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
