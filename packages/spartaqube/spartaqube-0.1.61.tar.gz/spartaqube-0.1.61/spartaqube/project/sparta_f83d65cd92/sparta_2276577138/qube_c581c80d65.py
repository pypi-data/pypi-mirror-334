_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_aac227c3fb.sparta_371b00b056 import qube_1f386c22b1 as qube_1f386c22b1
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_a362f1190b
def sparta_397807f0fe(request):A={'res':1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
@sparta_a362f1190b
def sparta_04dd2ecf2e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1f386c22b1.sparta_04dd2ecf2e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_d4675320c1(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_1f386c22b1.sparta_d4675320c1(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_a362f1190b
def sparta_d785cde231(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_1f386c22b1.sparta_d785cde231(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_a362f1190b
def sparta_fc96ff11a6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1f386c22b1.sparta_fc96ff11a6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_86652abf34(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1f386c22b1.sparta_86652abf34(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_eb1f0409c3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1f386c22b1.sparta_eb1f0409c3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_32a46579eb(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_1f386c22b1.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_a362f1190b
def sparta_65e9f0cd0e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1f386c22b1.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_2c944389b0(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_1f386c22b1.sparta_2c944389b0(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_cd0fd5ab3b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1f386c22b1.sparta_cd0fd5ab3b(A,C);E=json.dumps(D);return HttpResponse(E)