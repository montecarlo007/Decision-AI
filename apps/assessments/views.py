from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Quiz, Attempt
from apps.content.models import DocumentModel
import datetime
from bson import ObjectId

class QuizDetailView(View):
    def get(self, request, quiz_id):
        # Allow guests
        try:
            quiz = Quiz.objects.get(id=ObjectId(quiz_id))
        except Quiz.DoesNotExist:
             messages.error(request, 'Quiz not found')
             return redirect('dashboard')
             
        return render(request, 'assessments/quiz_take.html', {'quiz': quiz})

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=ObjectId(quiz_id))
        except Quiz.DoesNotExist:
             return redirect('dashboard')
             
        user_answers = []
        correct_count = 0
        total_questions = len(quiz.questions)
        
        for i, question in enumerate(quiz.questions):
            answer = request.POST.get(f'question_{i}', '')
            user_answers.append(answer)
            # Simple string matching for now. 
            # In production, handle case sensitivity and strip whitespace
            if answer and answer.strip().lower() == question.correct_answer.strip().lower():
                correct_count += 1
                
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        try:
            # Save Attempt
            attempt = Attempt(
                quiz=quiz,
                score=score,
                user_answers=user_answers,
                session_id=request.session.session_key or 'guest'
            )
            if request.user.is_authenticated:
                attempt.user = request.user
                
            attempt.save()
            return redirect('quiz_result', attempt_id=attempt.id)
            
        except Exception as e:
            print(f"Quiz Submission Error: {e}")
            messages.error(request, f"Error saving quiz result: {str(e)}")
            return redirect('dashboard')

class QuizResultView(View):
    def get(self, request, attempt_id):
        try:
            attempt = Attempt.objects.get(id=ObjectId(attempt_id))
        except Attempt.DoesNotExist:
            return redirect('dashboard')
            
        # Calculate progress circle offset (Circumference = 2 * pi * 88 ≈ 552.92)
        # offset = circumference - (circumference * score / 100)
        circumference = 552.92
        score = attempt.score if attempt.score else 0
        progress_offset = circumference - (circumference * score / 100)
        
        
        # Zip questions and answers for easier template rendering
        questions_and_answers = []
        if attempt.quiz and attempt.quiz.questions:
            questions = attempt.quiz.questions
            user_answers = attempt.user_answers or []
            # Ensure user_answers has same length by padding if necessary (though verify on save should prevent this)
            # But specific to this view logic:
            for i, question in enumerate(questions):
                answer = user_answers[i] if i < len(user_answers) else None
                questions_and_answers.append({
                    'question': question,
                    'user_answer': answer,
                    'is_correct': (answer and answer.strip().lower() == question.correct_answer.strip().lower())
                })

        return render(request, 'assessments/quiz_result.html', {
            'attempt': attempt,
            'progress_offset': progress_offset,
            'questions_and_answers': questions_and_answers
        })

class GenerateQuizView(View):
    def post(self, request, doc_id):
        try:
            doc = DocumentModel.objects.get(id=ObjectId(doc_id))
        except DocumentModel.DoesNotExist:
            messages.error(request, 'Document not found')
            return redirect('dashboard')
            
        difficulty = request.POST.get('difficulty', 'medium')
        try:
            num_questions = int(request.POST.get('num_questions', 5))
        except ValueError:
            num_questions = 5
            
        # Generate Quiz
        from apps.ai_core.services import OllamaService
        from apps.assessments.models import Quiz, Question
        
        ai_service = OllamaService()
        try:
            if not doc.extracted_text:
                messages.error(request, 'Document text not processed yet. Please retry processing.')
                return redirect('dashboard')

            quiz_data = ai_service.generate_quiz(doc.extracted_text, difficulty=difficulty, num_questions=num_questions)
            
            if 'questions' in quiz_data:
                quiz = Quiz(document=doc)
                questions = []
                VALID_TYPES = {'multiple_choice', 'true_false', 'open_ended', 'flashcard'}
                
                for q_data in quiz_data['questions']:
                    q_type = q_data.get('type', 'multiple_choice').lower().replace(' ', '_')
                    if q_type not in VALID_TYPES:
                        q_type = 'multiple_choice'
                        
                    q = Question(
                        type=q_type,
                        question=q_data.get('question', ''),
                        options=q_data.get('options', []),
                        correct_answer=q_data.get('correct_answer', ''),
                        explanation=q_data.get('explanation', ''),
                        tags=q_data.get('tags', []),
                        difficulty=q_data.get('difficulty', difficulty)
                    )
                    questions.append(q)
                quiz.questions = questions
                quiz.save()
                
                messages.success(request, f'Generated new {difficulty} quiz with {len(questions)} questions.')
                return redirect('quiz_detail', quiz_id=str(quiz.id))
            else:
                messages.error(request, 'Failed to generate quiz questions.')
        except Exception as e:
            print(f"Quiz Gen Error: {e}")
            messages.error(request, f'Error generating quiz: {str(e)}')
            
        return redirect('dashboard')
