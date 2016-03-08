"""
hashbattle URL Configuration
"""
from django.conf.urls import url, include, patterns
from rest_framework import routers
from django.contrib import admin

from battle_app import views


router = routers.DefaultRouter()
router.register(r'battles', views.BattleViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('battle_app.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/get-battle/(?P<id>[a-zA-Z0-9_.-]+)/$', views.BattleGet.as_view(), name='battle-get'),
    url(r'^get_input/$', views.get_user_input, name='get_user_input'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()