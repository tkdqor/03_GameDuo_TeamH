from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User as UserModel
from user.serializers import UserListSerializer, UserSigninSerializer, UserSignupSerializer


# /users/signup
class UserSignupApiView(APIView):
    """
    Assignee : 훈희

    회원가입 view 입니다.
    회원가입시 입력 data 타입 json 구조는 밑과 같습니다.
    {
        "nickname" : "test1",
        "password" : "root1234"
    }
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"messages": "가입 성공"}, status=status.HTTP_200_OK)
        else:
            return Response({"messages": "가입 실패"}, status=status.HTTP_400_BAD_REQUEST)


# /users/signin
class UserSigninApiView(APIView):
    """
    Assignee : 훈희

    로그인과 회원 전체 조회, 회원 단건 조회 기능입니다.
    로그인시 입력 data 타입 json 구조는 밑과 같습니다.
    {
        "nickname" : "test1",
        "password" : "root1234"
    }

    """

    permission_classes = [AllowAny]
    user_serializer = UserSigninSerializer

    def post(self, request):
        nickname = request.data.get("nickname", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=nickname, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)


class UserListAPIView(APIView):
    permission_classes = [IsAdminUser]
    user_serializer = UserListSerializer

    def get(self, request):
        """
        Assignee : 훈희

        플레이어 전체 목록이 나옵니다.
        해당 내용은 admin 유저만 확인 가능합니다.

        """
        all_user = UserModel.objects.all().order_by("last_login")
        serializer = UserSigninSerializer(all_user, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
