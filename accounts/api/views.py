from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from accounts.models import User, Donator, Worker, GoonjCenter, Volunteer
from .permissions import (
    IsAdminOrSuperUser,
    CustomOrIsAdminOrSuperUserPermission,
    IsSuperUserOrReadOnly,
    IsSuperUser)
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    DonatorSerializer,
    WorkerSerializer,
    GoonjCenterSerializer,
    VolunteerSerializer)

from rest_framework import generics, mixins


class OnlineUserAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = []

    def get_queryset(self):
        return User.objects.filter(is_online=True)


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


class GoonjCenterAPIView(generics.ListCreateAPIView):
    """
    Goonj Center related APIView
    get:
    Return list of all existing Goonj Centers with multiple information
      - Can Order by `?ordering=<field-name>` (for reverse add - at start, optional field)
      - Pagination support by `?limit=2` (optional)

    post:
    Creates a Goonj Center profile with given details
    """
    serializer_class = GoonjCenterSerializer
    permission_classes = (IsSuperUserOrReadOnly,)
    filter_backends = [OrderingFilter]
    pagination_class = LimitOffsetPagination

    # TODO: Add required filters for worker side based on frontend requirements
    def get_queryset(self):
        qs = GoonjCenter.objects.all()
        return qs

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GoonjCenterProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Goonj Center Profile information can be retrieved by super admin only
    get:
    Return that particular Goonj Center profile information

    put:
    Update any particular Goonj Center profile information

    delete:
    Delete that particular Goonj Center profile model Instance
    """
    lookup_field = 'pk'
    permission_classes = (IsSuperUser,)
    serializer_class = GoonjCenterSerializer

    def get_queryset(self):
        return GoonjCenter.objects.all()


# TODO: When creating worker or volunteer check if that particular user is actually worker or volunteer or not
# This can be done by making use of validate_pk maybe or validate_user_is_admin (not sure but easy)
class WorkerAPIView(generics.ListCreateAPIView):
    """
    Worker related APIView
    get:
    Return list of all existing worker with multiple information
      - Can Order by `?ordering=<field-name>` (for reverse add - at start, optional field)
      - Pagination support by `?limit=2` (optional)

    post:
    Creates a worker profile with given details
    """
    serializer_class = WorkerSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = [OrderingFilter]
    pagination_class = LimitOffsetPagination

    # TODO: Add required filters for worker side based on frontend requirements
    def get_queryset(self):
        qs = Worker.objects.all()
        return qs

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class WorkerProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Worker Profile information can be retrieved by admin or super admin
    get:
    Return that particular worker profile information

    put:
    Update any particular worker information

    delete:
    Delete that particular worker model Instance
    """
    lookup_field = 'pk'
    permission_classes = (IsAdminOrSuperUser,)
    serializer_class = WorkerSerializer

    def get_queryset(self):
        return Worker.objects.all()


class VolunteerAPIView(generics.ListCreateAPIView):
    """
    Volunteer related APIView
    get:
    Return list of all existing worker with multiple information
      - Can Order by `?ordering=<field-name>` (for reverse add - at start, optional field)
      - Pagination support by `?limit=2` (optional)

    post:
    Creates a Volunteer profile with given details
    """
    serializer_class = VolunteerSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = [OrderingFilter]
    pagination_class = LimitOffsetPagination

    # TODO: Add required filters for worker side based on frontend requirements
    def get_queryset(self):
        qs = Volunteer.objects.all()
        return qs

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VolunteerProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Volunteer Profile information can be retrieved by admin or super admin
    get:
    Return that particular Volunteer profile information

    put:
    Update any particular Volunteer information

    delete:
    Delete that particular Volunteer model Instance
    """
    lookup_field = 'pk'
    permission_classes = (IsAdminOrSuperUser,)
    serializer_class = VolunteerSerializer

    def get_queryset(self):
        return Volunteer.objects.all()

# TODO: Check if we really need to create an API service for admin or models for admin (Permission: Superadmin)
