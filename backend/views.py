from rest_framework.response import Response
from rest_framework.views import APIView


class Home(APIView):
    """
    Sample View to show whether the given API is live or not
    """
    permission_classes = []

    def get(self, request):
        return Response({'status': 200})
