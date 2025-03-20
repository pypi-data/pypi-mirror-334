from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_55deb7a658.sparta_22275198ce.qube_53336e0975.sparta_0df0a7337c'
handler500='project.sparta_55deb7a658.sparta_22275198ce.qube_53336e0975.sparta_8086ca160d'
handler403='project.sparta_55deb7a658.sparta_22275198ce.qube_53336e0975.sparta_83178f7c03'
handler400='project.sparta_55deb7a658.sparta_22275198ce.qube_53336e0975.sparta_d555d3595b'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]