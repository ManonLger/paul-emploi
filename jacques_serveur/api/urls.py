from rest_framework.routers import DefaultRouter

from api.views.fields import FieldsViewSet
from api.views.formation import FormationViewSet
from api.views.offer import OfferViewSet
from api.views.profile import ProfileViewSet
from api.views.user import UserViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet, base_name='offer')
router.register(r'profile', ProfileViewSet, base_name='profile')
router.register(r'fields', FieldsViewSet, base_name='field')
router.register(r'formations', FormationViewSet, base_name='formation')
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = router.urls
