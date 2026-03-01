from django.db import models
from pets.models import Pet
from datetime import timedelta

'''

Implementação: 

1 - Catálogo de Vacina
2 - Registro de Aplicação de Vacina

'''

#1. Catálogo de Vacinas disponíveis
class VaccineType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    reinforce_interval_days = models.IntegerField(default=365)

    def __str__(self):
        return self.name
    
#2. O registro efetivo da aplicação no Pet (Mantendo a função anterior)
class Vaccine(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccines'
    )
    
    # Vincular a vacina aplicada a um tipo específica do catálogo
    vaccine_type = models.ForeignKey(
        VaccineType,
        on_delete=models.PROTECT,
        related_name='applied_vaccines'
    )

    applied_at = models.DateField()
    next_dose = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    # Calcula a próxima dose automaticamente
    def save(self, *args, **kwargs):
        if not self.next_dose and self.vaccine_type.reinforce_interval_days:
            self.next_dose = self.applied_at + timedelta(days=self.vaccine_type.reinforce_interval_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vaccine_type.name} - {self.pet.name}"