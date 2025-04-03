from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SRQ20Resposta

class SRQ20RelatorioIndividualView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        respostas = SRQ20Resposta.objects.filter(user=request.user).order_by('-data_resposta')

        if not respostas.exists():
            return Response({"mensagem": "Nenhuma resposta encontrada."})

        ultima = respostas.first()

        try:
            soma = sum(ultima.respostas)
        except Exception:
            return Response({"erro": "Respostas inválidas ou corrompidas."}, status=400)

        interpretacao = "Sem indício de transtorno" if soma < 7 else "Possível transtorno mental"

        return Response({
            "usuario": request.user.email,
            "data": ultima.data_resposta.strftime('%d/%m/%Y %H:%M'),
            "respostas": ultima.respostas,
            "pontuacao": soma,
            "interpretacao": interpretacao
        })
