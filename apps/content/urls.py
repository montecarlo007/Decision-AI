from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadDocumentView.as_view(), name='upload'),
    path('summary/<str:doc_id>/', views.DocumentSummaryView.as_view(), name='document_summary'),
    path('flashcards/<str:doc_id>/', views.DocumentFlashcardsView.as_view(), name='document_flashcards'),
    path('process/<str:doc_id>/', views.ProcessDocumentView.as_view(), name='process_document'),
]
