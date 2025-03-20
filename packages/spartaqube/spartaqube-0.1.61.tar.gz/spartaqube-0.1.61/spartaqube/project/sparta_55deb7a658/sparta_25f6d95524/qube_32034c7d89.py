_L='bPublicUser'
_K='developer_name'
_J='developer_id'
_I='b_require_password'
_H='developer_obj'
_G='default_project_path'
_F='bCodeMirror'
_E='menuBar'
_D='dist/project/homepage/homepage.html'
_C='res'
_B=None
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import FileResponse,Http404
from urllib.parse import unquote
from django.conf import settings as conf_settings
import project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 as qube_4ed691eaf9
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_993310294e
from project.sparta_aac227c3fb.sparta_b84f45d953 import qube_5452acab62 as qube_5452acab62
from project.sparta_aac227c3fb.sparta_e0ad6143e8.qube_533d926758 import sparta_978905e1c8
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_bfddbd2e43(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_4ed691eaf9.sparta_74b58b0068(B);return render(B,_D,A)
	qube_5452acab62.sparta_924ece80bf();A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_E]=12;D=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(D);A[_F]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_978905e1c8();C=os.path.join(F,'developer');E(C);A[_G]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_dfe9cc1f49(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_4ed691eaf9.sparta_74b58b0068(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_5452acab62.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_bfddbd2e43(B)
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_E]=12;H=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(H);A[_F]=_A;F=E[_H];A[_G]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_4bc733ad5b(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_4ed691eaf9.sparta_74b58b0068(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_5452acab62.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_bfddbd2e43(B)
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_E]=12;H=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(H);A[_F]=_A;F=E[_H];A[_G]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_e267d73145(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)