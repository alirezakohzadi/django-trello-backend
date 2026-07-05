from rest_framework.routers import DefaultRouter
from .views import CardViewSet



router = DefaultRouter()
router.register("api", CardViewSet, basename="cards")


urlpatterns = router.urls
