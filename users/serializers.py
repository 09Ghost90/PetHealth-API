from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    telefone = serializers.CharField(write_only=True)
    endereco = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'telefone',
            'endereco',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        telefone = validated_data.pop('telefone')
        endereco = validated_data.pop('endereco')

        user = User.objects.create_user(**validated_data)

        tutor = user.tutor
        tutor.telefone = telefone
        tutor.endereco = endereco
        tutor.save()

        return user
