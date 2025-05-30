from django.urls import path
from . import views

urlpatterns = [
    path('<int:test_id>/start/', views.start_test, name='quiz-question'),
    path('<int:test_id>/submit/', views.submit_answer, name='quiz-submit'),
    path('', views.home, name='quiz-home'),
]
