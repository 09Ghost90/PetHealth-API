from rest_framework import serializers
from .models import Vaccine, VaccineType
from datetime import timedelta

class VaccineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineType
        fields = ['id', 'name', 'description', 'reinforce_interval_days']

class VaccineSerializer(serializers.ModelSerializer):
    # Mostra os detalhes do tipo da vacina (nome, descrição) na leitura (GET)
    vaccine_type_details = VaccineTypeSerializer(source='vaccine_type', read_only=True)

    # Campos: para mostrar o nome do pet e do tutor na leitura (GET)
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    tutor_name = serializers.CharField(
    source='pet.tutor.user.username',
    read_only=True
    )
    
    # Campo para receber apenas o ID do tipo da vacina na escrita (POST)
    vaccine_type_id = serializers.PrimaryKeyRelatedField(
        queryset=VaccineType.objects.all(),
        source='vaccine_type',
        write_only=True
    )

    class Meta:
        model = Vaccine
        fields = [
            'id',
            'pet',
            'pet_name',           # Campo extra para mostrar o nome do pet na leitura
            'tutor_name',         # Campo extra para mostrar o nome do tutor na leitura
            'vaccine_type_id',      # Entrada: ID do tipo
            'vaccine_type_details', # Saída: Objeto completo do tipo
            'applied_at',
            'next_dose',
        ]
        read_only_fields = ['next_dose', 'pet_name', 'tutor_name'] # Calculado com base no tipo da vacina e na data da aplicação

    def create(self, validated_data):
        # Lógica calculo do next_dose com base no tipo da vacina(VaccineType) e na data da aplicação
        vaccine_type = validated_data['vaccine_type']
        applied_at = validated_data['applied_at']
        
        # Se o usuário não enviou next_dose manualmente, calculamos
        if 'next_dose' not in validated_data:
            days = vaccine_type.reinforce_interval_days
            validated_data['next_dose'] = applied_at + timedelta(days=days)

        return super().create(validated_data)