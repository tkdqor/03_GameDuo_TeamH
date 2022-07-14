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


class RaidRecordModelSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    레이드 레코드의 값을 조회하여 값의 토탈을 만들고 레이드 레코드 값도 조회 가능
    추가적인 생성과 관련된 내용은 없이 데이터를 가공해서 보내주는 역할을 함

    """

    totalScore = serializers.SerializerMethodField(required=False, read_only=True)

    def get_totalScore(self, obj):
        balance = obj.raid_record.totalScore
        for record in obj.raid_record.user_raid_record.order_by("level", "enter_time").filter(is_deleted=False):
            if obj.user == obj.user:
                balance += record.amount
        return balance

    def create(self, validated_data):
        user_id = self.context["raid_record"]
        user_raid_record = RaidRecordModel(user=user_id, **validated_data)
        user_raid_record.save()
        return user_raid_record

    class Meta:
        model = RaidRecordModel
        fields = ("user", "level", "score", "enter_time", "end_time", "level_clear_score", "time_limit")
        read_only_fields = ["is_deleted"]


class RaidRecordSerializer(serializers.ModelSerializer):
    # article_set = articleSerializer(many=True)
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
    raid_records = serializers.SerializerMethodField(required=False, read_only=True)

    def get_total_score(self, obj):
        raid_records = RaidRecordModel.objects.filter(user_id=obj)
        total_score = 0
        for record in raid_records:
            total_score += record.level_clear_score
        return total_score

    def get_raid_records(self, obj):
        raid_records = RaidRecordModel.objects.filter(user_id=obj)

        return raid_records

    class Meta:
        model = UserModel
        fields = ("nickname", "total_score", "raid_records", "user_id")
        read_only_fields = ["nickname"]
