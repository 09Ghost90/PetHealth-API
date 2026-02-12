from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PetViewSet
from vaccines.views import VaccineViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pets')

# rota manual aninhada
pets_vaccines = [
    path(
        'pets/<int:pet_id>/vaccines/',
        VaccineViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='pet-vaccines'
    )
]

urlpatterns = router.urls + pets_vaccines