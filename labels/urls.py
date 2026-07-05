from rest_framework.routers import DefaultRouter

from .views import LabelViewSet



router = DefaultRouter()
router.register("api", LabelViewSet, basename="labels")


urlpatterns = router.urls
