_K='bPublicUser'
_J='notebook_name'
_I='notebook_id'
_H='b_require_password'
_G='notebook_obj'
_F='default_project_path'
_E='bCodeMirror'
_D='menuBar'
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
import project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 as qube_4ed691eaf9
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_993310294e
from project.sparta_aac227c3fb.sparta_e79e653f43 import qube_08f87dafb2 as qube_08f87dafb2
from project.sparta_aac227c3fb.sparta_e0ad6143e8.qube_533d926758 import sparta_978905e1c8
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_fb92f90a4a(request):
	B=request;A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_D]=13;D=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(D);A[_E]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_978905e1c8();C=os.path.join(F,'notebook');E(C);A[_F]=C;return render(B,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_0443376071(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_08f87dafb2.sparta_84281686a2(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_fb92f90a4a(B)
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_D]=12;H=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_414da11f38(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_08f87dafb2.sparta_84281686a2(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_fb92f90a4a(B)
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_D]=12;H=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)