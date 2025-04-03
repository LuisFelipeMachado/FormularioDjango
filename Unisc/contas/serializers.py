from rest_framework import serializers
from .models import SRQ20Resposta

class SRQ20RespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRQ20Resposta
        fields = ['id', 'respostas', 'data_resposta']

    def validate_respostas(self, value):
        if len(value) != 20:
            raise serializers.ValidationError("Você deve enviar exatamente 20 respostas.")
        if not all(answer in [0, 1] for answer in value):
            raise serializers.ValidationError("As respostas devem ser 0 (Não) ou 1 (Sim).")
        return value
