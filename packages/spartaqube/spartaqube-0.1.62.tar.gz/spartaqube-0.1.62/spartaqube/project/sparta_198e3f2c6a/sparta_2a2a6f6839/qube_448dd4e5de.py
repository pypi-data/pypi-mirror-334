_A='menuBar'
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
from project.sparta_c86ac10c1e.sparta_d3da874fba import qube_21fd14cf2a as qube_21fd14cf2a
from project.sparta_c86ac10c1e.sparta_1beb93e42a import qube_120f717b56 as qube_120f717b56
from project.sparta_c86ac10c1e.sparta_45f849ee34.qube_8460cefce9 import sparta_90ad52a9f3
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_ba41bf2147(request):A=request;B=qube_05f3410cc3.sparta_40b78ff765(A);B[_A]=-1;C=qube_05f3410cc3.sparta_7e34f10c40(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_a1c68064bc(request,kernel_manager_uuid):
	D=kernel_manager_uuid;C=True;B=request;E=False
	if D is None:E=C
	else:
		F=qube_21fd14cf2a.sparta_b14df55eaa(B.user,D)
		if F is None:E=C
	if E:return sparta_ba41bf2147(B)
	def H(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=C)
	K=sparta_90ad52a9f3();G=os.path.join(K,'kernel');H(G);I=os.path.join(G,D);H(I);J=os.path.join(I,'main.ipynb')
	if not os.path.exists(J):
		L=qube_120f717b56.sparta_5e7d7b354c()
		with open(J,'w')as M:M.write(json.dumps(L))
	A=qube_05f3410cc3.sparta_40b78ff765(B);A['default_project_path']=G;A[_A]=-1;N=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(N);A['kernel_name']=F.name;A['kernelManagerUUID']=F.kernel_manager_uuid;A['bCodeMirror']=C;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)