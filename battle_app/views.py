
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 

from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from .dictionary import TextAnalysis

import json


@csrf_exempt
def get_user_input(request):
    user_input = request.POST.get("user_input", "")
    analysis = TextAnalysis(user_input, 140)
    analysis.run()
    return HttpResponse(analysis.improved_text)
