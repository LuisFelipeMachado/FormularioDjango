from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model, authenticate
from .models import SRQ20Resposta
from .serializers import SRQ20RespostaSerializer

User = get_user_model()

# Função index corretamente indentada
def index_view(request):
    return render(request, 'contas/index.html')

def dashboard(request):
    return render(request, 'contas/dashboard.html')

def historico_view(request):
    return render(request, 'contas/historico.html')

def metricas_view(request):
    return render(request, 'contas/metricas.html')

def relatorios_view(request):
    return render(request, 'contas/relatorios.html')

def register_view(request):
    return render(request, 'contas/register.html')

# --------- REGISTRO ---------
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        nome = request.data.get("nome")
        password = request.data.get("password")
        genero = request.data.get("genero")
        idade = request.data.get("idade")

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email já existe"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, nome=nome, password=password)
        # Agora setamos os campos extras
        user.genero = genero
        user.idade = idade
        user.save()

        return Response({"message": "Usuário registrado com sucesso!"}, status=status.HTTP_201_CREATED)

# --------- LOGIN COM JWT ---------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login bem-sucedido!",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

# --------- ENVIAR RESPOSTAS SRQ-20 ---------
class EnviarSRQ20View(generics.CreateAPIView):
    serializer_class = SRQ20RespostaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# --------- LISTAR RESPOSTAS DO USUÁRIO ---------
class ListarSRQ20View(generics.ListAPIView):
    serializer_class = SRQ20RespostaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SRQ20Resposta.objects.filter(user=self.request.user)

# --------- RELATÓRIO INDIVIDUAL ---------
class SRQ20RelatorioIndividualView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        respostas = SRQ20Resposta.objects.filter(user=request.user)

        if not respostas.exists():
            return Response({"mensagem": "Nenhuma resposta encontrada."})

        ultima = respostas.latest("data_resposta")
        soma = sum(ultima.respostas)

        interpretacao = "Sem indício de transtorno" if soma < 7 else "Possível transtorno mental"

        return Response({
            "usuario": request.user.email,
            "data": ultima.data_resposta,
            "respostas": ultima.respostas,
            "pontuacao": soma,
            "interpretacao": interpretacao
        })

# --------- RELATÓRIO GERAL (com filtros) ---------
class SRQ20RelatorioGeralView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        respostas = SRQ20Resposta.objects.all()

        genero = request.query_params.get('genero')
        idade_min = request.query_params.get('idade_min')
        idade_max = request.query_params.get('idade_max')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        if genero:
            respostas = respostas.filter(user__genero=genero)
        if idade_min:
            respostas = respostas.filter(user__idade__gte=int(idade_min))
        if idade_max:
            respostas = respostas.filter(user__idade__lte=int(idade_max))
        if data_inicio:
            respostas = respostas.filter(data_resposta__date__gte=data_inicio)
        if data_fim:
            respostas = respostas.filter(data_resposta__date__lte=data_fim)

        total = respostas.count()
        if total == 0:
            return Response({"mensagem": "Nenhum dado disponível com os filtros aplicados."})

        somas = [sum(r.respostas) for r in respostas]
        media_sim = round(sum(somas) / total, 2)
        casos_suspeitos = len([s for s in somas if s >= 7])
        percentual_suspeitos = round((casos_suspeitos / total) * 100, 2)

        return Response({
            "total_respostas": total,
            "media_respostas_sim": media_sim,
            "usuarios_com_potencial_transtorno": casos_suspeitos,
            "percentual_de_risco": f"{percentual_suspeitos}%",
            "filtros_aplicados": {
                "genero": genero,
                "idade_min": idade_min,
                "idade_max": idade_max,
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        })

# --------- HISTÓRICO FILTRADO PARA DASHBOARD ---------
class SRQ20HistoricoFiltradoView(ListAPIView):
    serializer_class = SRQ20RespostaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = SRQ20Resposta.objects.filter(user=self.request.user)

        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')

        if data_inicio:
            queryset = queryset.filter(data_resposta__date__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_resposta__date__lte=data_fim)

        return queryset.order_by('-data_resposta')

       

