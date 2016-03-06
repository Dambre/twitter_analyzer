from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.all_battles, name='all_battles'),
    url(r'^get_input/$', views.get_user_input, name='get_user_input'),
]