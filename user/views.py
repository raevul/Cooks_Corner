from rest_framework import views, status, permissions
from rest_framework.response import Response


class RegisterAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({"data": "register"})
