from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from accounts.models import User, Donator
from .permissions import IsAdminOrSuperUser, CustomOrIsAdminOrSuperUserPermission
from .serializers import UserSerializer, UserProfileSerializer, DonatorSerializer

from rest_framework import generics, mixins, authentication, permissions


class UserAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    """
    User related APIView
    get:
    Return list of all existing users with multiple information
      - Can Order by `?ordering=<field-name>` (for reverse add - at start)
      - Pagination support by `?limit=2`

    post:
    Creates a user with given phone_number and password
    """
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = [OrderingFilter]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        email = self.request.GET.get("email")
        phone_number = self.request.GET.get("phone_number")
        first_name = self.request.GET.get("first_name")
        last_name = self.request.GET.get("last_name")
        gender = self.request.GET.get("gender")
        is_active = self.request.GET.get("is_active")
        is_admin = self.request.GET.get("is_admin")
        is_worker = self.request.GET.get("is_worker")
        is_volunteer = self.request.GET.get("is_volunteer")

        qs = User.objects.myfilter(
            email__icontains=email,
            phone_number__icontains=phone_number,
            first_name__icontains=first_name,
            last_name__icontains=last_name,
            gender__icontains=gender,
            is_active=is_active,
            is_admin=is_admin,
            is_worker=is_worker,
            is_volunteer=is_volunteer
        ).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Profile information can be retrieved here and can be shown by that particular
    authenticated user or any admin can do that
    get:
    Return that particular profile information

    put:
    Update any particular user information

    delete:
    Delete that particular user Instance, maybe can be used to deactivate the account
    """
    lookup_field = 'pk'
    permission_classes = (CustomOrIsAdminOrSuperUserPermission,)
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.all()


# TODO: Date started and date ended, between these days filter Donator
class DonatorAPIView(generics.ListCreateAPIView):
    """
    Donator related APIView
    get:
    Return list of all existing donator with multiple information
      - Can Order by `?ordering=<field-name>` (for reverse add - at start)
      - Pagination support by `?limit=2`

    post:
    Creates a donator profile with given details
    """
    serializer_class = DonatorSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [OrderingFilter]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        email = self.request.GET.get("email")
        phone_number = self.request.GET.get("phone_number")
        first_name = self.request.GET.get("first_name")
        last_name = self.request.GET.get("last_name")
        gender = self.request.GET.get("gender")

        qs = Donator.objects.myfilter(
            email__icontains=email,
            phone_number__icontains=phone_number,
            first_name__icontains=first_name,
            last_name__icontains=last_name,
            gender__icontains=gender,
        ).distinct()

        return qs

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DonatorProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Donator Profile information can be retrieved by any authenticated user
    get:
    Return that particular donator profile information

    put:
    Update any particular donator information

    delete:
    Delete that particular donator model Instance
    """
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)
    serializer_class = DonatorSerializer

    def get_queryset(self):
        return Donator.objects.all()

# TODO: Create API Service to directly create Worker (Permission: Admin/Superadmin)


# TODO: Create API Service to directly create Volunteer (Permission: Admin/Superadmin)


# TODO: Create API Service to directly create an Admin (Permission: Superadmin)
