from rest_framework import serializers

from boss_raid.models import RaidRecord as RaidRecordModel
from user.models import User as UserModel


class UserListSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    유저리스트 serializer 입니다.

    """

    class Meta:
        model = UserModel
        fields = ["id", "nickname"]


class UserSigninSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    로그인 serializer 입니다.

    """

    class Meta:
        model = UserModel
        fields = ["id", "nickname"]


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    회원가입 serializer 입니다.
    nickname에 대한 유효성 검사 password에 대한 유효성 검사를 수행
    create와 update를 지원합니다.

    """

    class Meta:
        model = UserModel
        fields = ["nickname", "password"]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data.get("nickname"):
            if not len(data.get("nickname", "")) >= 6:
                raise serializers.ValidationError(detail={"error": "nickname의 길이는 6자리 이상이어야 합니다."})

        if not len(data.get("password", "")) >= 6:
            raise serializers.ValidationError(detail={"error": "password의 길이는 6자리 이상이어야 합니다."})

        return data

    def create(self, validated_data):
        password = validated_data.pop("password", "")

        user = UserModel(**validated_data)

        """ pbkdf2 알고리즘 방식으로 비밀번호 암호화 """
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()

        return instance


class BossRaidHistorySerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    View단에서 user 모델의 객체가 주어졌을 때,
    역참조를 통해 raidRecord 모델의 쿼리셋을 가져오기

    """

    class Meta:
        model = RaidRecordModel

        fields = ["level", "score", "enter_time", "end_time", "level_clear_score", "time_limit"]


class UserListDetailSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    View단에서 user 모델의 객체가 주어졌을 때,
    역참조를 통해 raidRecord 모델의 쿼리셋을 가져오기

    """

    user_id = serializers.IntegerField(source="id", required=False, read_only=True)
    total_score = serializers.SerializerMethodField(required=False, read_only=True)
    boss_raid_history = serializers.SerializerMethodField(required=False, read_only=True)

    def get_total_score(self, obj):
        raid_records = RaidRecordModel.objects.filter(user_id=obj).all()
        total_score = 0
        for record in raid_records:
            total_score += record.level_clear_score
        return total_score

    def get_boss_raid_history(self, obj):
        raid_records = RaidRecordModel.objects.filter(user_id=obj.id)
        boss_raid_history_serializer = BossRaidHistorySerializer(raid_records, many=True)

        return boss_raid_history_serializer.data

    class Meta:
        model = UserModel
        fields = ("nickname", "total_score", "user_id", "boss_raid_history")
        read_only_fields = ["nickname"]
