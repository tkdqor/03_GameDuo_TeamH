from rest_framework import serializers

from user.models import User as UserModel


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    회원가입 serializer 입니다.

    """

    class Meta:
        model = UserModel
        fields = ["id", "nickname"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = UserModel(**validated_data)
        """set_password() 를 사용해 헤싱을 해준다."""
        user.set_password(password)
        user.save()

        return user.id


class UserSigninSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    로그인 serializer 입니다.

    """

    class Meta:
        model = UserModel
        fields = ["id", "nickname"]
