from rest_framework.routers import DefaultRouter 
from .views import ListViewSet

router = DefaultRouter()
router.register("api", ListViewSet, basename="boards")

urlpatterns = router.urls