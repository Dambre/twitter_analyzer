from django.contrib import admin
from .models import *

# Register your models here.
class BattleAdmin(admin.ModelAdmin):
    model = Battle
    readonly_fields = ('id',)
    exclude = ('hashtag1_score', 'hashtag2_score', 'score', 'winner', 'updated_time', 'ended')

admin.site.register(Battle, BattleAdmin)