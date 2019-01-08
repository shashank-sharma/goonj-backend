from django.shortcuts import render
from rest_framework.response import Response


# Create your views here.
from rest_framework.views import APIView



def home(request):
    return render(request, 'home.html', {})
# class Home(APIView):
#     """
#     Sample View to show whether the given API is live or not
#     """
#     permission_classes = []
#     def get(self, request):
#         return Response({'status': 200})