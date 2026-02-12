from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, ListField, ReferenceField
from django.contrib.auth.hashers import make_password, check_password
import datetime

class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    role = StringField(choices=('admin', 'user', 'guest'), default='user')
    is_active = BooleanField(default=True)
    date_joined = DateTimeField(default=datetime.datetime.utcnow)
    last_login = DateTimeField()
    
    # Guest specific
    is_guest = BooleanField(default=False)
    session_id = StringField()  # For tracking guests before registration

    meta = {'collection': 'users'}

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_staff(self):
        return self.role == 'admin'

    def has_perm(self, perm, obj=None):
        return self.role == 'admin'

    def has_module_perms(self, app_label):
        return self.role == 'admin'

    def __str__(self):
        return self.email
