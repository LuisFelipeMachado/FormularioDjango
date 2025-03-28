from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

# -------- REGISTRO --------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        nome = request.data.get("nome")
        password = request.data.get("password")

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email já existe"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(email=email, nome=nome, password=password)
        return Response({"message": "Usuário registrado com sucesso"}, status=status.HTTP_201_CREATED)


# -------- LOGIN --------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            return Response({"message": "Login bem-sucedido!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
