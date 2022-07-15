from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.jwt_claim_serializer import GameTokenObtainPairSerializer, RefreshTokenSerializer
from user.models import User as UserModel
from user.serializers import UserListDetailSerializer, UserListSerializer, UserSigninSerializer, UserSignupSerializer


# /users/signup
class UserSignupApiView(APIView):
    """
    Assignee : 훈희

    post : 회원가입
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


# /users/login
class LoginView(APIView):
    """
    Assignee : 훈희

    post : 로그인
    로그인 할때 access token과 refresh token을 함께 가져옴

    로그인시 입력 data 타입 json 구조는 밑과 같습니다.
    {
        "nickname" : "test1",
        "password" : "root1234"
    }

    delete : 로그아웃
    테스트등 개발 환경에서 사용하기 위한 간단한 로그아웃 기능
    토큰을 반납하지 않고 로그아웃이 됩니다.

    """

    permission_classes = [AllowAny]

    def post(self, request):
        nickname = request.data.get("nickname", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=nickname, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        user_serializer = UserSigninSerializer(user)
        token = GameTokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        response = Response(
            {
                "user": user_serializer.data,
                "message": "로그인 성공!!",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        login(request, user)
        return response

    def delete(self, request):
        user = request.user
        logout(request)
        return Response(f"user :{user} 로그아웃 성공!!, 토큰을 유지")


# /users/logout
class LogoutView(GenericAPIView):
    """
     Assignee : 훈희

     post : 로그아웃
     로그아웃 하면서 토큰을 같이 반납합니다.
     기존의 delete method를 사용하지 않으며 post 방식으로 refresh token을
     보내주게 됩니다.

     로그인시 입력 data 타입 json 구조는 밑과 같습니다.
    {
       "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NzkwMzY5MywiaWF0IjoxNjU3ODE3MjkzLCJqdGkiOiJkMjdiMGUxNDU1NTc0NWRjYWRiOTU4YzA1YjA4ZGEzNiIsInVzZXJfaWQiOjgsImlkIjo4LCJuaWNrbmFtZSI6InRlc3Q0MiJ9.iqLPbGoFxaFbp0yXvsKjBwgT7EF29I6URi7O05j2YVg"
    }

    """

    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        refresh = self.get_serializer(data=request.data)
        refresh.is_valid(raise_exception=True)
        refresh.save()

        user = request.user
        logout(request)

        return Response(f"user :{user} 로그아웃 성공!!, 토큰을 반납", status=status.HTTP_204_NO_CONTENT)


# /users/
class UserListAPIView(APIView):
    """
    Assignee : 훈희

    get : 회원 전체 조회
    플레이어 전체 목록이 나옵니다.
    해당 내용은 admin 유저만 확인 가능합니다.

    """

    permission_classes = [IsAdminUser]
    user_serializer = UserListSerializer

    def get(self, request):
        all_user = UserModel.objects.all().order_by("last_login")
        serializer = UserSigninSerializer(all_user, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# /users/api/gametoken
class GameTokenObtainPairView(TokenObtainPairView):
    """
    Assignee : 훈희

    커스텀 된 토큰 시리얼라이저 테스트용 View입니다.

    """

    serializer_class = GameTokenObtainPairSerializer


# /users/<user_id>
class UserListDetailAPIView(APIView):
    """
    Assignee : 훈희

    get : 유저 단건 조회
    totalScore와 bossRaidHistory가 표시되는 유저 단건 조회 입니다.
    밑의 response 구조에 맞춘 유저 단건 조회 입니다.

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
