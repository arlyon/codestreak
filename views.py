from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Streak

# Create your views here.

def index(request):
    template = loader.get_template('codestreak/index.html')
    code_streak = Streak.objects.filter(user=request.user).first()
    context = {
        'code_streak': code_streak.streak,
        'good': True,
    }
    if code_streak is None:
        if request.user.socialaccount_set.github is not None:
            s = Streak(streak=0, user=request.user)
            s.save()
            context["message"] = "You're all set up!"
        else:
            context["message"] = "Attach a github account to your profile and meet me here in 5!"
    return HttpResponse(template.render(context, request))