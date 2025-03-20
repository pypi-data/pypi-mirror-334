_A='menuBar'
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
from project.sparta_aac227c3fb.sparta_27abf0b36c import qube_f776bbbf13 as qube_f776bbbf13
from project.sparta_aac227c3fb.sparta_6ed1dc9d1a import qube_4a0322b5be as qube_4a0322b5be
from project.sparta_aac227c3fb.sparta_e0ad6143e8.qube_533d926758 import sparta_978905e1c8
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_6f821ad491(request):A=request;B=qube_4ed691eaf9.sparta_74b58b0068(A);B[_A]=-1;C=qube_4ed691eaf9.sparta_85b2d98a0f(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_45434efe90(request,kernel_manager_uuid):
	D=kernel_manager_uuid;C=True;B=request;E=False
	if D is None:E=C
	else:
		F=qube_f776bbbf13.sparta_4f7a5a6d1f(B.user,D)
		if F is None:E=C
	if E:return sparta_6f821ad491(B)
	def H(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=C)
	K=sparta_978905e1c8();G=os.path.join(K,'kernel');H(G);I=os.path.join(G,D);H(I);J=os.path.join(I,'main.ipynb')
	if not os.path.exists(J):
		L=qube_4a0322b5be.sparta_d3f4cdeb3b()
		with open(J,'w')as M:M.write(json.dumps(L))
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A['default_project_path']=G;A[_A]=-1;N=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(N);A['kernel_name']=F.name;A['kernelManagerUUID']=F.kernel_manager_uuid;A['bCodeMirror']=C;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)