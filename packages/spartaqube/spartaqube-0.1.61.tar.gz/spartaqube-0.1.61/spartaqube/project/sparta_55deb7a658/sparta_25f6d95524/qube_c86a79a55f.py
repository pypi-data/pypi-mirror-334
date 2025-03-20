import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 as qube_4ed691eaf9
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_993310294e
from project.sparta_aac227c3fb.sparta_88338b39fb import qube_2041d0ee11 as qube_2041d0ee11
from project.sparta_aac227c3fb.sparta_46ddce8369 import qube_64734ec0f9 as qube_64734ec0f9
def sparta_20ec5c7e66():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_fd0f826428(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_4ed691eaf9.sparta_74b58b0068(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A['menuBar']=12;F=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)