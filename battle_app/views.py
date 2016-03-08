
from django.shortcuts import render
from rest_framework import viewsets, generics
from django.core import management
from django.views.decorators.csrf import csrf_exempt 

from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from .twitter import count_hash
from .serializers import BattleSerializer
from .get_dictionary import analyze_post 

import json


def all_battles(request):
    # management.call_command('update_hash')
    return render(request, 'battle_app/index.html', {'battles': Battle.objects.all().order_by('-end_time')})
    

class BattleViewSet(viewsets.ModelViewSet):
    '''
    API for listing all battles
    '''
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer

class BattleGet(generics.ListCreateAPIView):
    serializer_class = BattleSerializer
    queryset = Battle.objects.all()
    def get_queryset(self):        
        """
        This view should return a battle by id
        """
        id = self.kwargs['id']
        queryset = self.queryset.filter(id=str(id))
        if queryset:
            b = queryset[0]
            count, updated_time = count_hash(
                [b.hashtag1,
                b.hashtag2],
                b.start_time,
                b.end_time,
                b.updated_time
                )
            b.hashtag1_score += count[b.hashtag1]
            b.hashtag2_score += count[b.hashtag2]
            b.updated_time = updated_time
            b.save()
            queryset = self.queryset.filter(id=str(id))
        return queryset

@csrf_exempt
def get_user_input(request):
    user_input = request.POST.get("user_input", "")
    return HttpResponse(user_input)
