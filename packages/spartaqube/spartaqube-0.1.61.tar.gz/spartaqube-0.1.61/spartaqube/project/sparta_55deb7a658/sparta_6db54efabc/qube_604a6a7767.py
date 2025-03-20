from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_993310294e
from project.sparta_aac227c3fb.sparta_1365f57f75 import qube_19ae54c804 as qube_19ae54c804
from project.models import UserProfile
import project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 as qube_4ed691eaf9
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_f97d7b9188(request):
	E='avatarImg';B=request;A=qube_4ed691eaf9.sparta_74b58b0068(B);A['menuBar']=-1;F=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_993310294e
@login_required(redirect_field_name='login')
def sparta_897c8fc063(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_f97d7b9188(A)