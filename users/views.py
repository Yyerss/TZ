from django.shortcuts import render
import requests
from django.views import View


# Create your views here.
class FetchUsers(View):
    api_url = "http://localhost:8000/api/v1/users/"

    def get(self, request):
        first_name = request.GET.get('first_name')
        params = {'first_name': first_name} if first_name else {}
        response = requests.get(self.api_url, params=params)
        users = response.json() if response.status_code == 200 else []
        return render(request, 'users/users_list.html', {'users': users})
