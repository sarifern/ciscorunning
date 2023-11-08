from .models import Profile
from allauth.account.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def get_avatar(request,user,*args, **kwargs):
    url = None
    user=kwargs.get('user')
    # if backend.name == 'facebook':
    #     url = response.get('picture').get('data').get('url')
    # if backend.name == 'instagram':
    #     url = response.get('user').get('profile_picture')
    # if backend.name == 'google-oauth2':
    #     url = response.get('picture')
    # if url:
    #     profile = Profile.objects.get_or_create(user=user)[0]
    #     profile.avatar = url
    #     profile.save()
    #     user.profile = profile
    #     user.save()