from django.conf.urls import url
from . import views

app_name = 'elections'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^areas/(?P<area>.+)/$', views.areas),
    url(r'^areas/(?P<area>.+)/results$', views.results),
    url(r'^polls/(?P<poll_id>\d+)/$', views.polls),  # 이 url에 대한 요청을 views.polls가 처리하게 만듭니다.
    url(r'^candidates/(?P<name>.+)/$', views.candidates),
]