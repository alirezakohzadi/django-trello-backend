from rest_framework.routers import DefaultRouter
from .views import CommentViewSet

router = DefaultRouter()

router.register("api", CommentViewSet, basename="comments")

urlpatterns = router.urls