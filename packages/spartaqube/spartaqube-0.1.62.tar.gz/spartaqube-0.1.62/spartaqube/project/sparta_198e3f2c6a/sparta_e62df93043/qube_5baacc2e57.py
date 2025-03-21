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
import project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 as qube_05f3410cc3
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_cbd160ca6d
from project.sparta_c86ac10c1e.sparta_12fa21ba06 import qube_a43e7f23a9 as qube_a43e7f23a9
from project.sparta_c86ac10c1e.sparta_45f849ee34.qube_8460cefce9 import sparta_90ad52a9f3
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_0bec370702(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_05f3410cc3.sparta_40b78ff765(B);return render(B,_D,A)
	qube_a43e7f23a9.sparta_ffb2da91fc();A=qube_05f3410cc3.sparta_40b78ff765(B);A[_E]=12;D=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(D);A[_F]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_90ad52a9f3();C=os.path.join(F,'developer');E(C);A[_G]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_cf4d59606e(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_05f3410cc3.sparta_40b78ff765(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_a43e7f23a9.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_0bec370702(B)
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_E]=12;H=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(H);A[_F]=_A;F=E[_H];A[_G]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_0c487051c7(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_05f3410cc3.sparta_40b78ff765(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_a43e7f23a9.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_0bec370702(B)
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_E]=12;H=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(H);A[_F]=_A;F=E[_H];A[_G]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_9c08fc3548(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)