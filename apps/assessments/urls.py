from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<str:quiz_id>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('result/<str:attempt_id>/', views.QuizResultView.as_view(), name='quiz_result'),
    path('generate/<str:doc_id>/', views.GenerateQuizView.as_view(), name='generate_quiz'),
]
