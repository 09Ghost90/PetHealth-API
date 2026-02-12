from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound

from .models import Vaccine
from .serializers import VaccineSerializer
from pets.models import Pet
from users.models import Tutor

class VaccineViewSet(ModelViewSet):
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pet_id = self.kwargs.get('pet_id')

        # Funcionario/admin vê tudo
        if user.is_staff:
            return Vaccine.objects.filter(pet_id=pet_id)
    
        if hasattr(user, 'tutor'):
            return Vaccine.objects.filter(
                pet_id=pet_id,
                pet__tutor=user.tutor
            )

        return Vaccine.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user

        # Somente funcionários podem registrar vacinas
        if not user.is_staff:
            raise PermissionDenied("Apenas funcionário podem registrar vacinas.")
        
        # Id do pet é fornecido na URL e não no body da requisição
        pet_id = self.kwargs.get('pet_id')

        if not pet_id:
            raise NotFound("Informe o ID do pet para registrar a vacina.")

        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            raise NotFound("Pet com o ID fornecido não existe.")

        serializer.save(pet=pet)