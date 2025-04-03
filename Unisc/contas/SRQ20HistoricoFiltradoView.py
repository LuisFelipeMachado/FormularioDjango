from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import SRQ20Resposta
from .serializers import SRQ20RespostaSerializer


class SRQ20HistoricoFiltradoView(ListAPIView):
    serializer_class = SRQ20RespostaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = SRQ20Resposta.objects.filter(user=user)

        data_inicio = self.request.query_params.get('data_inicio')  # Ex: 2024-01-01
        data_fim = self.request.query_params.get('data_fim')        # Ex: 2024-12-31

        if data_inicio:
            queryset = queryset.filter(data_resposta__date__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_resposta__date__lte=data_fim)

        return queryset.order_by('-data_resposta')
