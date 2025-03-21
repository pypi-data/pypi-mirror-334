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
import project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 as qube_05f3410cc3
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_cbd160ca6d
from project.sparta_c86ac10c1e.sparta_e7628d372d import qube_c0a1b95891 as qube_c0a1b95891
from project.sparta_c86ac10c1e.sparta_45f849ee34.qube_8460cefce9 import sparta_90ad52a9f3
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_8bca762e7f(request):
	B=request;A=qube_05f3410cc3.sparta_40b78ff765(B);A[_D]=13;D=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(D);A[_E]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_90ad52a9f3();C=os.path.join(F,'notebook');E(C);A[_F]=C;return render(B,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_832fd32cda(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_c0a1b95891.sparta_1f88e55cb9(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_8bca762e7f(B)
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_D]=12;H=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_004238b1a4(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_c0a1b95891.sparta_1f88e55cb9(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_8bca762e7f(B)
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_D]=12;H=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)