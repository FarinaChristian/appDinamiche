from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def quiz_home(request):
    return HttpResponse("Benvenuto nella sezione Quiz!")