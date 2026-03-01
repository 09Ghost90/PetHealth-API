from rest_framework import serializers
from .models import Pet
from datetime import date
from vaccines.models import Vaccine

class VaccineMiniSerializer(serializers.ModelSerializer):

    vaccine_name = serializers.CharField(source='vaccine_type.name', read_only=True)

    class Meta:
        model = Vaccine
        fields = [
            'id',
            'vaccine_name',
            'applied_at',
            'next_dose',
            'notes',
        ]


class PetSerializer(serializers.ModelSerializer):
    tutor_name = serializers.CharField(source='tutor.user.username', read_only=True)
    
    # Lista as vacinas do pet usando o VaccineMiniSerializer para mostrar apenas as informações essenciais
    vaccines = VaccineMiniSerializer(many=True, read_only=True)

    idade = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            'id',
            'name',
            'especie',
            'raca',
            'data_nascimento',
            'idade',
            'tutor_name',
            'vaccines',
        ]

    def get_idade(self, obj: Pet) -> int:
        if not obj.data_nascimento:
            return None
        today = date.today()
        return today.year - obj.data_nascimento.year - (
            (today.month, today.day) < (obj.data_nascimento.month, obj.data_nascimento.day)
        )