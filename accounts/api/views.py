from django.db.models import Q

from accounts.models import User
from .permissions import IsVolunteer, IsAdmin, IsSuperUser
from .serializers import UserSerializer

from rest_framework import generics, mixins

# mixins.CreateModelMixin,
class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsSuperUser)


    def get_queryset(self):
        qs = User.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(phone_number__icontains=query)
            ).distinct()

        return qs

    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
