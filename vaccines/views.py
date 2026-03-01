from rest_framework import viewsets, permissions
from .models import Vaccine, VaccineType
from .serializers import VaccineSerializer, VaccineTypeSerializer

class VaccineTypeViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para o Catálogo de Vacinas.
    Qualquer um autenticado pode ver, mas idealmente só admin deveria criar.
    """
    queryset = VaccineType.objects.all()
    serializer_class = VaccineTypeSerializer
    permission_classes = [permissions.IsAuthenticated] # Alterar aqui para permitir apenas admin criar/editar

class VaccineViewSet(viewsets.ModelViewSet):
    """
    Registro de vacinas aplicadas nos pets.
    """
    serializer_class = VaccineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtra para retornar apenas vacinas dos pets do usuário logado
        user = self.request.user
        if user.is_staff:
            return Vaccine.objects.all()
        return Vaccine.objects.filter(pet__tutor__user=user)