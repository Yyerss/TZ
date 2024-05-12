from django.shortcuts import render
from rest_framework import generics
from users.models import User
from .serializers import UserSerializer


# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        first_name = self.request.query_params.get('first_name')
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        return queryset
