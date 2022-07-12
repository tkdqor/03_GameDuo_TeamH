from django.urls import path

from .views import BossRaidStatusAPIView

app_name = "boss_raid"

urlpatterns = [
    path("api/v1/bossRaid", BossRaidStatusAPIView.as_view()),
]
