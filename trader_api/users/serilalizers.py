from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', 'type','first_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            password=validated_data['password'],
            type=validated_data.get('type', 'viewer'),
            email=validated_data['email'],
            first_name=validated_data['username']
        )
        return user

    def validate(self, attrs):
        unexpected_fields = set(self.initial_data.keys()) - set(self.fields)
        if unexpected_fields:
            raise serializers.ValidationError(
                {"detail": f"Campos inválidos fornecidos: {', '.join(unexpected_fields)}"}
            )

        return super().validate(attrs)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adiciona o nome do usuário ao payload do token
        token['name'] = user.username

        return token
    