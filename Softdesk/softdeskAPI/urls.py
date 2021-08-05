from django.urls import path
from .views import CreateUserAPIView, ListUserAPIView

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), name='create_user'),
    path('members/', ListUserAPIView.as_view(), name='member')
]
