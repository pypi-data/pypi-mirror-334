from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_cbd160ca6d
from project.sparta_c86ac10c1e.sparta_f524962c59 import qube_72b4ca2075 as qube_72b4ca2075
from project.models import UserProfile
import project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 as qube_05f3410cc3
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_d1975bddd9(request):
	E='avatarImg';B=request;A=qube_05f3410cc3.sparta_40b78ff765(B);A['menuBar']=-1;F=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_cbd160ca6d
@login_required(redirect_field_name='login')
def sparta_4bd1041fb4(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_d1975bddd9(A)