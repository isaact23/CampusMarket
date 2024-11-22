from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not value.endswith('@gmu.edu'):
            raise serializers.ValidationError('Email must be a valid GMU email address (@gmu.edu)')
        return value