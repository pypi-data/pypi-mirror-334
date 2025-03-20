_O='Please send valid data'
_N='dist/project/auth/resetPasswordChange.html'
_M='captcha'
_L='password'
_K='POST'
_J=False
_I='login'
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 as qube_4ed691eaf9
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_993310294e
from project.sparta_aac227c3fb.sparta_24405b5ac7 import qube_651f37dbb3 as qube_651f37dbb3
from project.sparta_f83d65cd92.sparta_f1bc4afd8e import qube_fa3a138048 as qube_fa3a138048
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_e59f028ada():return{'bHasCompanyEE':-1}
def sparta_824d08a698(request):B=request;A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_C]=qube_4ed691eaf9.sparta_368d53e99d();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_993310294e
def sparta_8fca3ec5cd(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_b9d9279ddf(C,A)
def sparta_7422ded1f0(request,redirectUrl):return sparta_b9d9279ddf(request,redirectUrl)
def sparta_b9d9279ddf(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_651f37dbb3.sparta_e31221964a(F):return sparta_824d08a698(A)
				login(A,F);K,L=qube_4ed691eaf9.sparta_95c81a5e3f();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_4ed691eaf9.sparta_74b58b0068(A);B.update(qube_4ed691eaf9.sparta_1f1d991a29(A));B[_C]=qube_4ed691eaf9.sparta_368d53e99d();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_e59f028ada());return render(A,'dist/project/auth/login.html',B)
def sparta_eb228d1fa7(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_993310294e
def sparta_66531785ba(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_651f37dbb3.sparta_756547b696()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_651f37dbb3.sparta_526b4cf4c2(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_651f37dbb3.sparta_06aa966634(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_4ed691eaf9.sparta_74b58b0068(A);C.update(qube_4ed691eaf9.sparta_1f1d991a29(A));C[_C]=qube_4ed691eaf9.sparta_368d53e99d();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_e59f028ada());return render(A,'dist/project/auth/registration.html',C)
def sparta_1357f50de0(request):A=request;B=qube_4ed691eaf9.sparta_74b58b0068(A);B[_C]=qube_4ed691eaf9.sparta_368d53e99d();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_4a3350d30f(request,token):
	A=request;B=qube_651f37dbb3.sparta_cd3e44709f(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_4ed691eaf9.sparta_74b58b0068(A);D[_C]=qube_4ed691eaf9.sparta_368d53e99d();return redirect(_I)
def sparta_f31a14283b(request):logout(request);return redirect(_I)
def sparta_f8d1b02f8f(request):
	A=request;from project.models import PlotDBChartShared as C,PlotDBChart;B='cypress_tests@gmail.com';print('Destroy cypress user');D=C.objects.filter(user__email=B).all()
	for E in D:E.delete()
	if A.user.is_authenticated:
		if A.user.email==B:A.user.delete()
	logout(A);return redirect(_I)
def sparta_d48da48595(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_1649502119(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_651f37dbb3.sparta_1649502119(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_4ed691eaf9.sparta_74b58b0068(A);C.update(qube_4ed691eaf9.sparta_1f1d991a29(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_4ed691eaf9.sparta_368d53e99d();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_4ed691eaf9.sparta_74b58b0068(A);D.update(qube_4ed691eaf9.sparta_1f1d991a29(A));D[_C]=qube_4ed691eaf9.sparta_368d53e99d();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_e59f028ada());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_351c945738(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_651f37dbb3.sparta_351c945738(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_4ed691eaf9.sparta_74b58b0068(D);A.update(qube_4ed691eaf9.sparta_1f1d991a29(D));A[_C]=qube_4ed691eaf9.sparta_368d53e99d();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_e59f028ada());return render(D,_N,A)