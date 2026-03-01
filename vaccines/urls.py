from rest_framework.routers import DefaultRouter
from .views import VaccineViewSet
from vaccines.views import VaccineViewSet, VaccineTypeViewSet

router = DefaultRouter()
router.register(r'vaccines', VaccineViewSet, basename='vaccine')

# Registrando o ViewSet para VaccineType
router.register(r'vaccine-types', VaccineTypeViewSet)
router.register(r'vaccine-types', VaccineTypeViewSet, basename='vaccine-type')

urlpatterns = router.urls