_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='res'
_C='Content-Disposition'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_c86ac10c1e.sparta_b1ebcd8f91 import qube_a70a5fd95a as qube_a70a5fd95a
from project.sparta_c86ac10c1e.sparta_b1ebcd8f91 import qube_bfe36e89ea as qube_bfe36e89ea
from project.sparta_c86ac10c1e.sparta_45f849ee34 import qube_9cbbe19431 as qube_9cbbe19431
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_4be367f918
@csrf_exempt
@sparta_4be367f918
def sparta_e305bc23bb(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_a70a5fd95a.sparta_13e25989c6(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_4be367f918
def sparta_177d31a107(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a70a5fd95a.sparta_5d1b2268fb(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_47c181ec9c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a70a5fd95a.sparta_1b5632e509(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_82e625f33f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a70a5fd95a.sparta_81bad4cc52(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_2fe3be03eb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_bfe36e89ea.sparta_8487b82d0d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_6f3a6454c7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a70a5fd95a.sparta_81add413d9(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_7f8549ea96(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a70a5fd95a.sparta_50e0fa1c4d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_62d4bf1619(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a70a5fd95a.sparta_bbd67a5598(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_d9db984a43(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a70a5fd95a.sparta_7071e0f8ec(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4be367f918
def sparta_4ee76d06ae(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_a70a5fd95a.sparta_8d66f90825(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_4be367f918
def sparta_2ff5e62a8c(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_a70a5fd95a.sparta_5a663d2d74(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_4be367f918
def sparta_da9eda1785(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_a70a5fd95a.sparta_9b3528fcef(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A