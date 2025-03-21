_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_c86ac10c1e.sparta_1beb93e42a import qube_da519e5270 as qube_da519e5270
from project.sparta_c86ac10c1e.sparta_1beb93e42a import qube_f82fa51e45 as qube_f82fa51e45
from project.sparta_c86ac10c1e.sparta_433a8e7b64 import qube_4ec6b7e2b1 as qube_4ec6b7e2b1
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_4be367f918,sparta_da7e56a063
@csrf_exempt
def sparta_b99d61fa1f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_b99d61fa1f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_a70364c2f4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_a70364c2f4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_617d39cfee(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_617d39cfee(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_6a06f2e4b6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_6a06f2e4b6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_436036f5f7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_436036f5f7(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_acead68576(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_acead68576(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_ee1caedf99(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_ee1caedf99(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_af5277cbac(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_af5277cbac(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_c56a943c4a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_c56a943c4a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_77698c5faa(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.sparta_77698c5faa(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_ea7d9755cc(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_da519e5270.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_a6a2be4e5a(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_da519e5270.sparta_a6a2be4e5a(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_41d0729cb6(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_b9675473b6(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_4be367f918
def sparta_72bed79afc(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_b9675473b6(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_da519e5270.sparta_8d66f90825(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_4be367f918
def sparta_84e9a6a44c(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_da519e5270.sparta_9b3528fcef(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_b86b43302c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_b86b43302c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_29c00f3546(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_29c00f3546(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_b920e0e771(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_b920e0e771(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_33bf13b09d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_33bf13b09d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_31fe71a81c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_31fe71a81c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_0ac60668d4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_0ac60668d4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_8462467eb1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_8462467eb1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_9e6d1e4779(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_9e6d1e4779(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_fb6be459f4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_fb6be459f4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_9ec72f500f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_9ec72f500f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_8f78016bd8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_8f78016bd8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_8370358fa4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_8370358fa4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_a96939b83e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_a96939b83e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
@sparta_da7e56a063
def sparta_39becda479(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f82fa51e45.sparta_39becda479(C,A.user);E=json.dumps(D);return HttpResponse(E)