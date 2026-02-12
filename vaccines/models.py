from django.db import models
from pets.models import Pet

class Vaccine(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccines'
    )

    name = models.CharField(max_length=100)
    applied_at = models.DateField()
    next_dose = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.pet.name}"