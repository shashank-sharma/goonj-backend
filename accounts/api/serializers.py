from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from accounts.models import User, Donator, Worker, Volunteer, GoonjCenter


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'email',
            'first_name',
            'last_name',
            'gender',
            'is_admin',
            'is_worker',
            'is_volunteer',
            'date_joined',
            'avatar',
        ]
        read_only_fields = ['pk', 'date_joined']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'gender',
            'is_admin',
            'is_worker',
            'is_volunteer',
            'date_joined',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['pk']

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("Email should be unique")
        return value

    # TODO: Finalize phone number structure
    def validate_phone_number(self, value):
        if value[0] == '+':
            value = value[1:]
        if 8 <= len(value) <= 10:
            return value

    # TODO: Validate password based on numbers, special characters, uniqueness
    def validate_password(self, value: str) -> str:
        if len(value) < 7:
            raise serializers.ValidationError("Password Length should be greater than 8")
        else:
            return make_password(value)


class DonatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donator
        fields = [
            'pk',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'gender',
            'date_joined'
        ]
        read_only_fields = ['pk', 'date_joined']


class GoonjCenterSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoonjCenter
        fields = [
            'pk',
            'is_dropping_center',
            'address',
            'city',
            'country',
            'start_time',
            'end_time'
        ]


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = [
            'pk',
            'user',
            'goonj_center'
        ]

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['goonj_center'] = GoonjCenterSerializer(read_only=True)
        return super(WorkerSerializer, self).to_representation(instance)


class VolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteer
        fields = [
            'pk',
            'user',
            'donating_session_active',
            'goonj_center'
        ]

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['goonj_center'] = GoonjCenterSerializer(read_only=True)
        return super(VolunteerSerializer, self).to_representation(instance)
