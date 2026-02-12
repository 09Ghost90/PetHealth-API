from django.db import models
from users.models import Tutor

class Pet(models.Model):
    name = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50)
    data_nascimento = models.DateField(null=True, blank=True)

    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
        related_name='pets'
    )

    def __str__(self):
        return f"{self.name} ({self.especie})"