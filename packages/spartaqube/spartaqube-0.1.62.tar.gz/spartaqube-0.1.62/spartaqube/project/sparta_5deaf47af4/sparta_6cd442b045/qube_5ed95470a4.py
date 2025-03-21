_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_c86ac10c1e.sparta_e6b12a1d61 import qube_b0ec55220f as qube_b0ec55220f
from project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 import sparta_e5fee403ee
from project.logger_config import logger
@csrf_exempt
def sparta_e7289f2633(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_b0ec55220f.sparta_e7289f2633(B)
@csrf_exempt
def sparta_041cf60374(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_165db8e1d7(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_2182a69e63(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)