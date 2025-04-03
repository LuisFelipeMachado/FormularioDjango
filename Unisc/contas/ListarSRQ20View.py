from rest_framework import filters

class ListarSRQ20View(generics.ListAPIView):
    serializer_class = SRQ20RespostaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['data_resposta']
    ordering = ['-data_resposta']  # mais recentes primeiro

    def get_queryset(self):
        return SRQ20Resposta.objects.filter(user=self.request.user)
