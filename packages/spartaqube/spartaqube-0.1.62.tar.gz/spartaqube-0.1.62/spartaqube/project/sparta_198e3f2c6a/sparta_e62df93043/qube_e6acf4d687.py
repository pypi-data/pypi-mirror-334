import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 as qube_05f3410cc3
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_cbd160ca6d
from project.sparta_c86ac10c1e.sparta_d3a4fd1e04 import qube_af72c7c492 as qube_af72c7c492
from project.sparta_c86ac10c1e.sparta_433a8e7b64 import qube_4ec6b7e2b1 as qube_4ec6b7e2b1
def sparta_6e22f4088b():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_823875956a(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_05f3410cc3.sparta_40b78ff765(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_05f3410cc3.sparta_40b78ff765(B);A['menuBar']=12;F=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)