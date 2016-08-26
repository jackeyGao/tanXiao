from django.shortcuts import render
from django.shortcuts import render_to_response

from dsauth.models import UserProfile

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        user = request.user
        profile = UserProfile.objects.get(user=user)

    return render_to_response("index.html", locals())
