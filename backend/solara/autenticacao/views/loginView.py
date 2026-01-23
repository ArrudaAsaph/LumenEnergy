from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from autenticacao.serializers import LoginRequest
from autenticacao.serializers import LoginResponse
from autenticacao.services import LoginService

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = LoginService.login(serializer.validated_data)

        response = LoginResponse(result)
        return Response(response.data)
