from django.db.models import Q

from accounts.models import User
from .permissions import IsVolunteer, IsAdmin, IsSuperUser, IsAdminOrSuperUser
from .serializers import UserSerializer

from rest_framework import generics, mixins


class UserAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)

    def get_queryset(self):
        qs = User.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(phone_number__icontains=query)
            ).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
