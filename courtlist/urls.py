from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings

from courtlist import views
from django.conf.urls.static import static


urlpatterns=[
     # url('^$',views.index, name = 'index'),
     url(r'^$', views.home, name='home'),
     url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
     url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
     url(r'^signup/$', views.signup, name='signup'),
     url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
     url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),

]

if settings.DEBUG:
   urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
