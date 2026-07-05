from rest_framework.routers import DefaultRouter
from .views import AttachmentViewSet

router = DefaultRouter()
router.register("api", AttachmentViewSet, basename="attachments")

urlpatterns = router.urls