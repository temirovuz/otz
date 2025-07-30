from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from account.api.serializers import LoginSerializer, LogoutSerializer


@method_decorator(csrf_exempt, name="dispatch")
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request):
        data = request.data.copy()
        data["access"] = str(request.auth) if request.auth else None

        serializer = LogoutSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = serializer.save()
        return Response(
            result,
            status=(
                status.HTTP_205_RESET_CONTENT
                if result["success"]
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
        )
