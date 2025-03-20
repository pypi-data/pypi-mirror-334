_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_aac227c3fb.sparta_24405b5ac7 import qube_651f37dbb3 as qube_651f37dbb3
from project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 import sparta_6f00ce0a1c
from project.logger_config import logger
@csrf_exempt
def sparta_06aa966634(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_651f37dbb3.sparta_06aa966634(B)
@csrf_exempt
def sparta_65b7f91454(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_c780a4ccca(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_aa7f4b9035(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)