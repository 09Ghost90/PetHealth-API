from rest_framework import serializers
from .models import Vaccine

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = [
            'id',
            "name",
            'applied_at',
            'next_dose',
            'notes',
        ]
        read_only_fields = ['id']