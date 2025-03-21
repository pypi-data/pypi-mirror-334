_C='bCodeMirror'
_B='menuBar'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 as qube_05f3410cc3
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_cbd160ca6d
from project.sparta_c86ac10c1e.sparta_d3a4fd1e04 import qube_af72c7c492 as qube_af72c7c492
from project.sparta_c86ac10c1e.sparta_433a8e7b64 import qube_4ec6b7e2b1 as qube_4ec6b7e2b1
from project.sparta_c86ac10c1e.sparta_45f849ee34.qube_8460cefce9 import sparta_90ad52a9f3
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_ff91f3525b(request):
	B=request;C=B.GET.get('edit')
	if C is None:C='-1'
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_B]=9;E=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(E);A[_C]=_A;A['edit_chart_id']=C
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	G=sparta_90ad52a9f3();D=os.path.join(G,'dashboard');F(D);A['default_project_path']=D;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_8a0452ceb5(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_e8b0cf5d5a(A,B)
def sparta_e8b0cf5d5a(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_4ec6b7e2b1.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_ff91f3525b(B)
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_B]=9;I=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(I);A[_C]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)