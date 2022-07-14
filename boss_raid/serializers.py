from rest_framework.serializers import ModelSerializer

from .models import RaidRecord


class RaidRecordModelSerializer(ModelSerializer):
    """
    Assignee : 민지

    RaidRecord 모델을 위한 시리얼라이저 입니다.
    """

    def create(self, validated_data):
        return RaidRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.score = validated_data.get("score", instance.score)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.save()
        return instance

    class Meta:
        model = RaidRecord
        fields = "__all__"
