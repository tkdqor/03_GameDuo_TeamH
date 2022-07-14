from django.contrib import admin

from .models import BossRaid, RaidRecord


class RaidRecordModelAdmin(admin.ModelAdmin):
    readonly_fields = ("enter_time",)


admin.site.register(BossRaid)
admin.site.register(RaidRecord, RaidRecordModelAdmin)
