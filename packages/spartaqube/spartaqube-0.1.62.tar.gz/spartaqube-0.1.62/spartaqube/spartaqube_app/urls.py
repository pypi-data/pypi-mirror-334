from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_198e3f2c6a.sparta_9a9ec34654.qube_200da24f60.sparta_d8d0e19553'
handler500='project.sparta_198e3f2c6a.sparta_9a9ec34654.qube_200da24f60.sparta_65f4db8122'
handler403='project.sparta_198e3f2c6a.sparta_9a9ec34654.qube_200da24f60.sparta_c881d00a82'
handler400='project.sparta_198e3f2c6a.sparta_9a9ec34654.qube_200da24f60.sparta_1e84b93863'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]