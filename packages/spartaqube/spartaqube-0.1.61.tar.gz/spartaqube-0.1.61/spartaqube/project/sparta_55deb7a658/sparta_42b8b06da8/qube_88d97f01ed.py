_C='bCodeMirror'
_B='menuBar'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 as qube_4ed691eaf9
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_993310294e
from project.sparta_aac227c3fb.sparta_88338b39fb import qube_2041d0ee11 as qube_2041d0ee11
from project.sparta_aac227c3fb.sparta_46ddce8369 import qube_64734ec0f9 as qube_64734ec0f9
from project.sparta_aac227c3fb.sparta_e0ad6143e8.qube_533d926758 import sparta_978905e1c8
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_2b195bca09(request):
	B=request;C=B.GET.get('edit')
	if C is None:C='-1'
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_B]=9;E=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(E);A[_C]=_A;A['edit_chart_id']=C
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	G=sparta_978905e1c8();D=os.path.join(G,'dashboard');F(D);A['default_project_path']=D;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_c7f2f0085c(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_d0c3fbf7be(A,B)
def sparta_d0c3fbf7be(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_64734ec0f9.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_2b195bca09(B)
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_B]=9;I=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(I);A[_C]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)