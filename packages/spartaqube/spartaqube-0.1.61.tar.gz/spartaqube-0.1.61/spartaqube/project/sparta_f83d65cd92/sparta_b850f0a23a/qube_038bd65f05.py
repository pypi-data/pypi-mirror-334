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
from project.sparta_aac227c3fb.sparta_fe1bd3fe84 import qube_ba0f494cf0 as qube_ba0f494cf0
from project.sparta_aac227c3fb.sparta_fe1bd3fe84 import qube_5363fc9231 as qube_5363fc9231
from project.sparta_aac227c3fb.sparta_e0ad6143e8 import qube_cb17db70d7 as qube_cb17db70d7
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_a362f1190b
@csrf_exempt
@sparta_a362f1190b
def sparta_c3100dc702(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_ba0f494cf0.sparta_2935f1d06d(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_a362f1190b
def sparta_0b7778fa4a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ba0f494cf0.sparta_7b3a230bfe(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_e320c526b1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ba0f494cf0.sparta_553f0678c4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_195c42f285(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ba0f494cf0.sparta_ff88a233ce(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_6488fdaa76(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_5363fc9231.sparta_53c884394c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_f2b7926e05(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ba0f494cf0.sparta_3d4ddb517e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_cc9b2cb1ac(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ba0f494cf0.sparta_f07953f9c1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_e2d1a4e702(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ba0f494cf0.sparta_48d12220dd(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_a3f1552848(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ba0f494cf0.sparta_0c56324bd7(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a362f1190b
def sparta_469f6e0e24(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_ba0f494cf0.sparta_890dd61d2f(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_a362f1190b
def sparta_e5fe43ba92(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_ba0f494cf0.sparta_6b542b334e(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_a362f1190b
def sparta_c787a97bad(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_ba0f494cf0.sparta_1579ffc29d(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A