from .views import historico_view, metricas_view, relatorios_view
from .views import index_view, dashboard, register_view
from . import views
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    EnviarSRQ20View,
    ListarSRQ20View,
    SRQ20RelatorioIndividualView,
    SRQ20RelatorioGeralView,
    SRQ20HistoricoFiltradoView,  # 👈 adiciona essa linha
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # Página inicial
    path('', index_view, name='index'), 
    path('dashboard/', views.dashboard, name='dashboard'),

    # 🔐 Autenticação
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # 🔑 JWT padrão (caso queira usar com frontend)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🧠 Questionário SRQ-20
    path('srq20/enviar/', EnviarSRQ20View.as_view(), name='srq20-enviar'),
    path('srq20/minhas/', ListarSRQ20View.as_view(), name='srq20-listar'),

    # 📊 Relatórios e métricas
    path('srq20/relatorio/individual/', SRQ20RelatorioIndividualView.as_view(), name='srq20-relatorio-individual'),
    path('srq20/relatorio/geral/', SRQ20RelatorioGeralView.as_view(), name='srq20-relatorio-geral'),

    path('dashboard/historico/', SRQ20HistoricoFiltradoView.as_view(), name='dashboard-historico'),


    path('dashboard/historico/', historico_view, name='dashboard-historico'),
    path('dashboard/metricas/', metricas_view, name='dashboard-metricas'),
    path('dashboard/relatorios/', relatorios_view, name='dashboard-relatorios'),

    # Rota para exibir o HTML bonitão
    path('register/', register_view, name='register'),

    # Rota da API que recebe os dados via POST
    path('api/register/', RegisterView.as_view(), name='api-register'),
]
