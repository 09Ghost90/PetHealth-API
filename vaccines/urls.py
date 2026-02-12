from rest_framework.routers import DefaultRouter
from .views import VaccineViewSet

router = DefaultRouter()
router.register(r'vaccines', VaccineViewSet, basename='vaccine')

urlpatterns = router.urls