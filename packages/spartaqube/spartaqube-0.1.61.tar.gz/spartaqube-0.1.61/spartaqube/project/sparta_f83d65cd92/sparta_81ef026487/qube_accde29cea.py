_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_aac227c3fb.sparta_6ed1dc9d1a import qube_264182e3f7 as qube_264182e3f7
from project.sparta_aac227c3fb.sparta_6ed1dc9d1a import qube_b03fed69c3 as qube_b03fed69c3
from project.sparta_aac227c3fb.sparta_46ddce8369 import qube_64734ec0f9 as qube_64734ec0f9
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_a362f1190b,sparta_afc9e300b0
@csrf_exempt
def sparta_ca7cea0786(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_ca7cea0786(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_647ba9a4a1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_647ba9a4a1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_e156b5e1c8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_e156b5e1c8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_f3a646f269(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_f3a646f269(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_df9f88824a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_df9f88824a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_5fbed2ef79(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_5fbed2ef79(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_f4d892c9e2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_f4d892c9e2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_853641be1e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_853641be1e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_9933a109f9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_9933a109f9(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_e3bfa731be(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.sparta_e3bfa731be(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_b1f96e8d35(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_264182e3f7.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_fc7414dbe3(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_264182e3f7.sparta_fc7414dbe3(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_8ba2390dbe(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_0ba50aefc1(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_a362f1190b
def sparta_b126261003(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_0ba50aefc1(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_264182e3f7.sparta_890dd61d2f(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_a362f1190b
def sparta_fa1bfc6ace(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_264182e3f7.sparta_1579ffc29d(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_289fb1b0ba(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_289fb1b0ba(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_bf0dc52660(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_bf0dc52660(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_fd59c0b64d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_fd59c0b64d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_74aa5d4d0a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_74aa5d4d0a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_fa5b3ef3af(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_fa5b3ef3af(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_770ba527a1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_770ba527a1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_f9c55bc867(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_f9c55bc867(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_05a937c035(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_05a937c035(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_9653bc59f3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_9653bc59f3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_873ec736e7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_873ec736e7(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_a0689b24f2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_a0689b24f2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_de1e0c89c7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_de1e0c89c7(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_92276b8d62(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_92276b8d62(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
@sparta_afc9e300b0
def sparta_d8db4c5274(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b03fed69c3.sparta_d8db4c5274(C,A.user);E=json.dumps(D);return HttpResponse(E)