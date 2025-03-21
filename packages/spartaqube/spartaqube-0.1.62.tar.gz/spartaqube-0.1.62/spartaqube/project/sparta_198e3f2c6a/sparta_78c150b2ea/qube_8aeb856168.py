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
import project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 as qube_05f3410cc3
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_cbd160ca6d
from project.sparta_c86ac10c1e.sparta_e6b12a1d61 import qube_b0ec55220f as qube_b0ec55220f
from project.sparta_5deaf47af4.sparta_6cd442b045 import qube_5ed95470a4 as qube_5ed95470a4
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_d671736089():return{'bHasCompanyEE':-1}
def sparta_7eb15f650f(request):B=request;A=qube_05f3410cc3.sparta_40b78ff765(B);A[_C]=qube_05f3410cc3.sparta_031845dffd();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_cbd160ca6d
def sparta_72c2c163e3(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_ff8b7345ec(C,A)
def sparta_45f726e839(request,redirectUrl):return sparta_ff8b7345ec(request,redirectUrl)
def sparta_ff8b7345ec(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_b0ec55220f.sparta_943b9dea84(F):return sparta_7eb15f650f(A)
				login(A,F);K,L=qube_05f3410cc3.sparta_54923d83c8();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_05f3410cc3.sparta_40b78ff765(A);B.update(qube_05f3410cc3.sparta_8c35cb3fcb(A));B[_C]=qube_05f3410cc3.sparta_031845dffd();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_d671736089());return render(A,'dist/project/auth/login.html',B)
def sparta_9c38f78dd2(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_cbd160ca6d
def sparta_9e610bf845(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_b0ec55220f.sparta_a4d989c46a()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_b0ec55220f.sparta_c6effd195a(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_b0ec55220f.sparta_e7289f2633(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_05f3410cc3.sparta_40b78ff765(A);C.update(qube_05f3410cc3.sparta_8c35cb3fcb(A));C[_C]=qube_05f3410cc3.sparta_031845dffd();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_d671736089());return render(A,'dist/project/auth/registration.html',C)
def sparta_e6add16f4e(request):A=request;B=qube_05f3410cc3.sparta_40b78ff765(A);B[_C]=qube_05f3410cc3.sparta_031845dffd();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_f563ddcdc0(request,token):
	A=request;B=qube_b0ec55220f.sparta_7f77713d73(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_05f3410cc3.sparta_40b78ff765(A);D[_C]=qube_05f3410cc3.sparta_031845dffd();return redirect(_I)
def sparta_29f000fb86(request):logout(request);return redirect(_I)
def sparta_581bed07ce(request):
	A=request;from project.models import PlotDBChartShared as C,PlotDBChart;B='cypress_tests@gmail.com';print('Destroy cypress user');D=C.objects.filter(user__email=B).all()
	for E in D:E.delete()
	if A.user.is_authenticated:
		if A.user.email==B:A.user.delete()
	logout(A);return redirect(_I)
def sparta_88856fa079(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_0377b1a68f(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_b0ec55220f.sparta_0377b1a68f(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_05f3410cc3.sparta_40b78ff765(A);C.update(qube_05f3410cc3.sparta_8c35cb3fcb(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_05f3410cc3.sparta_031845dffd();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_05f3410cc3.sparta_40b78ff765(A);D.update(qube_05f3410cc3.sparta_8c35cb3fcb(A));D[_C]=qube_05f3410cc3.sparta_031845dffd();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_d671736089());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_45df2eb6af(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_b0ec55220f.sparta_45df2eb6af(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_05f3410cc3.sparta_40b78ff765(D);A.update(qube_05f3410cc3.sparta_8c35cb3fcb(D));A[_C]=qube_05f3410cc3.sparta_031845dffd();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_d671736089());return render(D,_N,A)