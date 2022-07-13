from django.urls import path

from .views import BossRaidEnterAPIView, BossRaidStatusAPIView

app_name = "boss_raid"

urlpatterns = [
    path("api/v1/bossRaid", BossRaidStatusAPIView.as_view()),
    path("api/v1/bossRaid/enter", BossRaidEnterAPIView.as_view()),
]
