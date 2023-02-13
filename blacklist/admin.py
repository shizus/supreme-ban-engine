
from django.contrib import admin

from blacklist.models import Game, PlayerReport


class GameAdmin(admin.ModelAdmin):
    """ Game view in admin page """
    pass


class PlayerAdmin(admin.ModelAdmin):
    """ Player view in admin page """
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(PlayerReport, PlayerAdmin)
