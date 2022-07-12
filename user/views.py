from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSigninSerializer, UserSignupSerializer


# /users/signup
class UserSiginupApiView(APIView):
    """
    Assignee : 훈희

    회원가입 view 입니다.
    회원가입시 입력 data 타입은 json 구조는 밑과 같습니다.
    {
        "nickname" : "test1",
        "password" : "root1234"
    }
    """

    permission_classes = [AllowAny]

    def post(self, request):
        user_serializer = UserSignupSerializer(data=request.data)

        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response({"messages": "가입 성공"}, status=status.HTTP_200_OK)

        else:
            # print(serializers.errors)
            return Response({"messages": "가입 실패"})


# /users/signin
class UserSigninApiView(APIView):
    """
    Assignee : 훈희

    로그인과 회원 전체 조회, 회원 단건 조회 기능입니다.
    로그인시 입력 data 타입은 json 구조는 밑과 같습니다.
    {
        "nickname" : "test1",
        "password" : "root1234"
    }

    """

    permission_classes = [AllowAny]
    user_serializer = UserSigninSerializer

    def get(self, request):
        user = request.user

        return Response(UserSigninSerializer(user).data, status=status.HTTP_200_OK)

    def post(self, request):
        nickname = request.data.get("nickname", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=nickname, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)
