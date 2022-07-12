from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# /users/login
class UserApiView(APIView):
    """
    Assignee : 훈희

    로그인을 지원하는 view 입니다.

    """

    def post(self, request):
        nickname = request.data.get("nickname", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=nickname, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)
