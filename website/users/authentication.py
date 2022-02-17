from django.contrib.auth.models import User


class CustomBackendAuthentication(object):
    """Custom authentication system using email address"""
    def authenticate(self, request, username=None, password=None):
        """Custom authenticate method"""
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Custom get_user method"""
        try:
            user_id = User.objects.get(pk=user_id)
            return user_id
        except User.DoesNotExist:
            return None
