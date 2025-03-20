_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_aac227c3fb.sparta_b36539732e import qube_2ad23ce490 as qube_2ad23ce490
from project.sparta_aac227c3fb.sparta_1365f57f75 import qube_19ae54c804 as qube_19ae54c804
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_a362f1190b
@csrf_exempt
@sparta_a362f1190b
def sparta_e7e5fb553d(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_19ae54c804.sparta_403dbf2780(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_2ad23ce490.sparta_e7e5fb553d(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_a362f1190b
def sparta_5a575fafb0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2ad23ce490.sparta_95447c535c(C,A.user);E=json.dumps(D);return HttpResponse(E)