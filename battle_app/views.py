
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

from .models import *
from .dictionary import TextAnalysis

import json


def index(request):
	return render(request, 'battle_app/index.html')
@require_POST
def get_user_input(request):
    user_input = request.POST.get("user_input", "")
    analysis = TextAnalysis(user_input, 140)
    analysis.run()
    return HttpResponse(analysis.improved_text)
