from django.contrib.auth.models import User

from .models import Profile


class EmailAuthBackend(object):
    """
    Authenticate using the user email.
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)

            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def social_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        try:
            profile = user.profile
        except AttributeError:
            profile = Profile(user=user)
            profile.save()