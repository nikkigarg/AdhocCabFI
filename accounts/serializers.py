from rest_framework import serializers

from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    # full_name = serializers.ReadOnlyField(source='get_full_name', default='')

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_first_login', 'created_by',
                  'updated_by', 'updated_on', 'created_on', 'is_temp_active')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'address', 'avatar', 'phone1', 'phone2')
