from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SRQ20Resposta

class SRQ20RelatorioGeralView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        respostas = SRQ20Resposta.objects.all()

        # 🔍 Filtros via query params
        genero = request.query_params.get('genero')
        idade_min = request.query_params.get('idade_min')
        idade_max = request.query_params.get('idade_max')
        data_inicio = request.query_params.get('data_inicio')  # YYYY-MM-DD
        data_fim = request.query_params.get('data_fim')        # YYYY-MM-DD

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
                "data_fim": data_fim,
            }
        })
