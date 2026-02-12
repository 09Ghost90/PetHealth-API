from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Pet
from .serializers import PetSerializer
from users.models import Tutor

class PetViewSet(ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Admin/funcionário vê todos os pets
        if user.is_staff:
            return Pet.objects.all()

        # Tutor comum vê apenas seus pets
        tutor, _ = Tutor.objects.get_or_create(user=user)
        return Pet.objects.filter(tutor=tutor)

    def perform_create(self, serializer):
        tutor, _ = Tutor.objects.get_or_create(user=self.request.user)
        serializer.save(tutor=tutor)