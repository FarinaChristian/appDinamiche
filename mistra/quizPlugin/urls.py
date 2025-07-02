from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:test_id>/', views.initiate_test, name='quiz-start'),
    path('question/', views.start_test, name='quiz-question'),
    path('submit/', views.submit_answer, name='quiz-submit'),
    path('completed/<str:revision_code>/', views.test_completed_view, name='quiz-completed'),
    path('', views.home, name='quiz-home'),
]
