_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_c86ac10c1e.sparta_dab21a590a import qube_8483d04bbc as qube_8483d04bbc
from project.sparta_c86ac10c1e.sparta_f524962c59 import qube_72b4ca2075 as qube_72b4ca2075
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_4be367f918
@csrf_exempt
@sparta_4be367f918
def sparta_6e7edd7e54(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_72b4ca2075.sparta_c1e6d0a50f(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_8483d04bbc.sparta_6e7edd7e54(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_4be367f918
def sparta_61f6845802(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8483d04bbc.sparta_a011f34607(C,A.user);E=json.dumps(D);return HttpResponse(E)