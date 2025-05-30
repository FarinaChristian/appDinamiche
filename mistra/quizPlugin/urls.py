from django.urls import path
from .views import *

urlpatterns = [
    path('', quiz_home, name='quiz_home'),
]
