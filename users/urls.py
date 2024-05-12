from django.urls import path
from .views import FetchUsers

urlpatterns = [
    path('', FetchUsers.as_view(), name='fetch-users'),
]