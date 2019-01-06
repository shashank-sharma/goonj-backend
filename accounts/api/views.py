from django.db.models import Q

from accounts.models import User
from .permissions import IsVolunteer, IsAdmin, IsSuperUser, IsAdminOrSuperUser
from .serializers import UserSerializer

from rest_framework import generics, mixins


# TODO: Update, destroy service needs to be created
# TODO: Add queryset like worker=true, volunteer=true and more
class UserAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    """
    User related APIView
    get:
    Return list of all existing users with multiple information

    post:
    Creates a user with given phone_number and password
    """
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


# TODO: Create API Service to directly create Worker (Permission: Admin/Superadmin)


# TODO: Create API Service to directly create Volunteer (Permission: Admin/Superadmin)


# TODO: Create API Service to directly create an Admin (Permission: Superadmin)
