from mongoengine import Document, EmbeddedDocument, StringField, ListField, ReferenceField, DateTimeField, IntField, FloatField, BooleanField, EmbeddedDocumentField
import datetime
from apps.users.models import User
from apps.content.models import DocumentModel

class Question(EmbeddedDocument):
    type = StringField(choices=('multiple_choice', 'true_false', 'open_ended', 'flashcard'), required=True)
    question = StringField(required=True)
    options = ListField(StringField())
    correct_answer = StringField(required=True)
    explanation = StringField()
    tags = ListField(StringField())
    difficulty = StringField(choices=('easy', 'medium', 'hard'), default='medium')

class Quiz(Document):
    document = ReferenceField(DocumentModel, required=True)
    questions = ListField(EmbeddedDocumentField(Question))
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    difficulty_level = StringField(default='medium') # Initial difficulty

    meta = {'collection': 'quizzes'}

class Attempt(Document):
    user = ReferenceField(User) # Optional for guests? "Guest attempts must be stored anonymously... with session tracking."
    # We can use session_id for guests if user is None
    session_id = StringField() 
    quiz = ReferenceField(Quiz, required=True)
    score = FloatField(default=0.0)
    user_answers = ListField(StringField()) # Store answers in order
    completed_at = DateTimeField(default=datetime.datetime.utcnow)
    time_taken = IntField() # seconds

    meta = {'collection': 'attempts'}
