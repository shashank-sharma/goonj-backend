from django.db.models import Q

from accounts.models import User
from .permissions import IsAdminOrSuperUser, CustomOrIsAdminOrSuperUserPermission
from .serializers import UserSerializer, UserProfileSerializer

from rest_framework import generics, mixins, authentication, permissions


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


class UserProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Profile information can be retrieved here and can be shown by that particular
    authenticated user or any admin can do that
    get:
    Return that particular profile information

    put:
    Update any particular user information
    """
    lookup_field = 'pk'
    permission_classes = (CustomOrIsAdminOrSuperUserPermission,)
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.all()

# TODO: Create API Service to directly create Worker (Permission: Admin/Superadmin)


# TODO: Create API Service to directly create Volunteer (Permission: Admin/Superadmin)


# TODO: Create API Service to directly create an Admin (Permission: Superadmin)
