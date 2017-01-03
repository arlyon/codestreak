from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Streak

# Create your views here.

def index(request):
    template = loader.get_template('codestreak/index.html')
    code_streak = Streak.objects.filter(user=request.user).first()
    context = {}
    if code_streak is not None:
        context["streak"] = code_streak.streak
        if code_streak.streak == 10:
            context["message"] = "Ten days in a row is impressive!"
        elif code_streak.streak == 25:
            context["message"] = "Twenty five days, that's a habit!"
        elif code_streak.streak == 50:
            context["message"] = "FIFTY DAYS! SHIIIIT"
        elif code_streak.streak == 100:
            context["message"] = "One hundred days! Contact me /u/alexthelyon with your story!"
        elif code_streak.streak == 200:
            context["message"] = "Holy shit dude. Reddit gold if you want it /u/alexthelyon."
        elif code_streak.streak == 500:
            context["message"] = "WTF 500 days!?"
        elif code_streak.streak == 1000:
            context["message"] = "JESUS CHRIST 1000 DAYS"
        else:
            context["message"] = "welcome"
        if code_streak.lost:
            context["lost"] = code_streak.lost
            context["message"] = "You slipped up after {0} days!".format(code_streak.streak)
            code_streak.streak = 0
            code_streak.lost = False
            code_streak.save()
    else:
        s = Streak(user=request.user)
        s.save()
        context["message"] = "I hope this will keep you motivated."
        context["streak"] = 0
    return HttpResponse(template.render(context, request))


def update_timezone(request):
    if request.method == "POST":
        try:
            item = Streak.objects.filter(user=request.user).first()
            offset = int(-round(int(request.POST.get("offset")), 0)/60 % 24)
            item.utc_offset = offset
            item.save()
            return JsonResponse({'message': 'success'})
        except:
            pass
    return JsonResponse({'message': 'fail'})


def quit(request):
    if request.method == "POST":
        Streak.objects.filter(user=request.user).delete()
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'fail'})