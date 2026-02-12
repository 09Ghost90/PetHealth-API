from rest_framework import serializers
from .models import Pet
from datetime import date
from vaccines.models import Vaccine

class VaccineMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = [
            'id',
            'name',
            'applied_at',
            'next_dose',
            'notes',
        ]


class PetSerializer(serializers.ModelSerializer):
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
            'vaccines',
        ]

    def get_idade(self, obj):
        today = date.today()
        return today.year - obj.data_nascimento.year