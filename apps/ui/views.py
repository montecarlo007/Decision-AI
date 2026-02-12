from django.shortcuts import render, redirect
from django.views import View
from apps.content.models import DocumentModel
from apps.assessments.models import Attempt
from apps.analytics.services import generate_student_performance_chart, generate_admin_stats

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'ui/home.html')

class DashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
            
        # Get recent documents
        documents = list(DocumentModel.objects(user=request.user).order_by('-uploaded_at')[:10])
        
        # Attach latest quiz to each doc for the UI
        from apps.assessments.models import Quiz
        for doc in documents:
            latest_quiz = Quiz.objects(document=doc).order_by('-created_at').first()
            if latest_quiz:
                doc.latest_quiz_id = str(latest_quiz.id)
            else:
                doc.latest_quiz_id = None
        
        # Get recent attempts
        attempts = Attempt.objects(user=request.user).order_by('-completed_at')[:5]
        
        # Get Analytics Chart
        try:
            performance_chart = generate_student_performance_chart(request.user.id)
        except Exception as e:
            performance_chart = None
            print(f"Analytics Error: {e}")

        context = {
            'documents': documents,
            'attempts': attempts,
            'performance_chart': performance_chart
        }
        return render(request, 'ui/dashboard.html', context)

class AdminDashboardView(View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('dashboard')
            
        stats = generate_admin_stats()
        return render(request, 'ui/admin_dashboard.html', {'stats': stats})
