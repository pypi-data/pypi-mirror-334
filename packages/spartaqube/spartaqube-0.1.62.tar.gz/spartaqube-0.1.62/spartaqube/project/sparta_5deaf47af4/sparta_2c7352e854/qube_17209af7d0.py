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
from project.sparta_c86ac10c1e.sparta_e8adbf5dc7 import qube_66399d4b90 as qube_66399d4b90
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_4be367f918
def sparta_94504e7b2c(request):A={'res':1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
@sparta_4be367f918
def sparta_b924526541(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_66399d4b90.sparta_b924526541(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_9cc2912da4(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_66399d4b90.sparta_9cc2912da4(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_4be367f918
def sparta_0363fcc76d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_66399d4b90.sparta_0363fcc76d(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_4be367f918
def sparta_0b4d9712b4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_66399d4b90.sparta_0b4d9712b4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_ca5a78d15d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_66399d4b90.sparta_ca5a78d15d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_a0647f5a0d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_66399d4b90.sparta_a0647f5a0d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_e1336286e1(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_66399d4b90.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_4be367f918
def sparta_392dc4a2ad(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_66399d4b90.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_5fa4873c7e(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_66399d4b90.sparta_5fa4873c7e(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_14648ac687(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_66399d4b90.sparta_14648ac687(A,C);E=json.dumps(D);return HttpResponse(E)