from rest_framework import serializers
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the User profile data.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_of_birth', 'profile_image']
        read_only_fields = ['id', 'username']
