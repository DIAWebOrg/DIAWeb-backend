from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView

class IndexView(APIView):
    def get(self, request):
        return HttpResponse("Welcome to my Django project!")


class HelloWorldView(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Hello World'})
