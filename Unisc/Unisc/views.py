from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

User = get_user_model()

# -------- REGISTRO --------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        nome = request.data.get("nome")
        senha = request.data.get("senha")

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email já cadastrado"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(email=email, nome=nome, password=senha)
        return Response({"message": "Usuário registrado com sucesso!"}, status=status.HTTP_201_CREATED)


# -------- LOGIN (JWT) --------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD  # usa o email no lugar do username

    def validate(self, attrs):
        email = attrs.get("email")
        senha = attrs.get("password")

        user = User.objects.filter(email=email).first()

        if user and user.check_password(senha):
            data = super().validate({"username": user.email, "password": senha})
            return data

        raise serializers.ValidationError("Email ou senha inválidos.")

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
