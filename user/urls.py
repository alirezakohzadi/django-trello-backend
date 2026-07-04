from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CreateUserView


urlpatterns = [
    path("create/", CreateUserView.as_view(), name="user-register"),
    path('create/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('update/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

