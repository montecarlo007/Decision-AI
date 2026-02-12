from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from .models import User
from bson import ObjectId

def get_user(request):
    if not hasattr(request, '_cached_user'):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                request._cached_user = User.objects.get(id=ObjectId(user_id))
            except User.DoesNotExist:
                request._cached_user = AnonymousUser()
        else:
            request._cached_user = AnonymousUser()
    return request._cached_user

class MongoAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
        return self.get_response(request)
