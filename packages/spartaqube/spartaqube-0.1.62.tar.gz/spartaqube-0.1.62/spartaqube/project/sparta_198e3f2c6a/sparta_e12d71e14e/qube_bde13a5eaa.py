from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 as qube_05f3410cc3
from project.models import UserProfile
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_cbd160ca6d
from project.sparta_198e3f2c6a.sparta_78c150b2ea.qube_8aeb856168 import sparta_d671736089
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_783bc4b0dd(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_05f3410cc3.sparta_40b78ff765(B);A.update(qube_05f3410cc3.sparta_7e34f10c40(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_d671736089());return render(B,'dist/project/auth/settings.html',A)