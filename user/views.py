from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.jwt_claim_serializer import GameTokenObtainPairSerializer
from user.models import User as UserModel
from user.serializers import UserListDetailSerializer, UserListSerializer, UserSigninSerializer, UserSignupSerializer


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

    def delete(self, request):
        user = request.user
        logout(request)
        return Response(f"로그아웃 되었습니다.{user}님 안녕히가세요!")


# /users/
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


# /api/gametoken
class GameTokenObtainPairView(TokenObtainPairView):
    serializer_class = GameTokenObtainPairSerializer


class UserListDetailAPIView(APIView):
    """
    Assignee : 훈희

    permission = 모두 가능
    Http method = GET
    GET : 유저 단건 조회

    response
    {
        totalScore:number,
            bossRaidHistory: [
            { raidRecordId:number, score:number, enterTime:string, endTime:string },
            //..
        ]
    }

    """

    permission_classes = [AllowAny]

    def get_object_and_check_permission(self, obj_id):
        """
        Assignee : 훈희

        obj_id : int

        input 인자로 단일 오브젝트를 가져오고, 퍼미션 검사를 하는 메서드입니다.
        DoesNotExist 에러 발생 시 None을 리턴합니다.
        """
        try:
            object = UserModel.objects.get(id=obj_id)
        except UserModel.DoesNotExist:
            return

        self.check_object_permissions(self.request, object)
        return object

    def get(self, request, user_id):
        """
        Assignee : 훈희

        obj_id : int

        유저 단일 조회를 하기 위한 메서드입니다.
        """
        user = self.get_object_and_check_permission(user_id)

        if not user:
            return Response({"error": "해당 유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        return Response(UserListDetailSerializer(user).data, status=status.HTTP_200_OK)
