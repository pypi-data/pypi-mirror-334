from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 as qube_4ed691eaf9
from project.models import UserProfile
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_993310294e
from project.sparta_55deb7a658.sparta_cf2881257e.qube_3e20a38b10 import sparta_e59f028ada
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_54f3f9419f(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_4ed691eaf9.sparta_74b58b0068(B);A.update(qube_4ed691eaf9.sparta_85b2d98a0f(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_e59f028ada());return render(B,'dist/project/auth/settings.html',A)