from django.views import View
from django.shortcuts import render
from .services import generate_student_performance_chart, generate_admin_stats
from apps.users.models import User

class StudentAnalyticsView(View):
    def get(self, request):
        chart = generate_student_performance_chart(request.user.id)
        return render(request, 'analytics/student_dashboard.html', {'performance_chart': chart})

class AdminAnalyticsView(View):
    def get(self, request):
        # Ensure admin
        if not request.user.is_staff:
             return render(request, '403.html') # Or redirect
             
        stats = generate_admin_stats()
        return render(request, 'analytics/admin_dashboard.html', {'stats': stats})
