from rest_framework.response import Response


# Create your views here.
from rest_framework.views import APIView


class Home(APIView):
    permission_classes = []
    def get(self, request):
        return Response({'status': 200})