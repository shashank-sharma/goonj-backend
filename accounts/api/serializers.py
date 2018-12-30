from rest_framework import serializers

from accounts.models import User


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
            'date_joined',
        ]
        read_only_fields = ['user', 'pk', 'date_joined']

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("Email should be unique")
        return value
