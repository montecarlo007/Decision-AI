from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import DocumentModel
from .tasks import process_document_task

class UploadDocumentView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'content/upload.html')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
            
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            messages.error(request, 'No file selected')
            return redirect('upload')

        # Determine file type
        filename = uploaded_file.name.lower()
        if filename.endswith('.pdf'):
            file_type = 'pdf'
        elif filename.endswith('.docx'):
            file_type = 'docx'
        elif filename.endswith('.txt'):
            file_type = 'txt'
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            file_type = 'image'
        else:
            messages.error(request, 'Unsupported file type')
            return redirect('upload')

        # Create Document
        doc = DocumentModel(
            user=request.user,
            title=uploaded_file.name,
            file_type=file_type
        )
        doc.file.put(uploaded_file, content_type=uploaded_file.content_type)
        doc.save()

        # Trigger Task (Run synchronously to avoid Redis dependency)
        try:
            process_document_task(str(doc.id))
        except Exception as e:
            print(f"Task Execution Error: {e}")
            messages.warning(request, 'Document saved but AI processing failed. Check logs.')

        messages.success(request, 'File uploaded successfully! Processing started.')
        return redirect('dashboard')

class ProcessDocumentView(View):
    def post(self, request, doc_id):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            process_document_task(doc_id)
            messages.success(request, 'AI processing completed!')
        except Exception as e:
            messages.error(request, f'Processing failed: {e}')
            
        return redirect('dashboard')

class DocumentSummaryView(View):
    def get(self, request, doc_id):
        if not request.user.is_authenticated:
            return redirect('login')
            
        from .models import SummaryModel
        doc = DocumentModel.objects.get(id=doc_id)
        summary = SummaryModel.objects(document=doc).first()
        
        return render(request, 'content/summary.html', {'doc': doc, 'summary': summary})

class DocumentFlashcardsView(View):
    def get(self, request, doc_id):
        if not request.user.is_authenticated:
            return redirect('login')
            
        from .models import Flashcard
        doc = DocumentModel.objects.get(id=doc_id)
        flashcards = Flashcard.objects(document=doc)
        
        return render(request, 'content/flashcards.html', {'doc': doc, 'flashcards': flashcards})
