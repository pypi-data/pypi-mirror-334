_O='serialized_data'
_N='has_access'
_M='plot_name'
_L='plot_chart_id'
_K='dist/project/plot-db/plotDB.html'
_J='edit_chart_id'
_I='edit'
_H='plot_db_chart_obj'
_G=False
_F='login'
_E='-1'
_D='bCodeMirror'
_C='menuBar'
_B=None
_A=True
import json,base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 as qube_4ed691eaf9
from project.sparta_aac227c3fb.sparta_24405b5ac7.qube_651f37dbb3 import sparta_993310294e
from project.sparta_aac227c3fb.sparta_88338b39fb import qube_2041d0ee11 as qube_2041d0ee11
from project.sparta_aac227c3fb.sparta_46ddce8369 import qube_64734ec0f9 as qube_64734ec0f9
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name=_F)
def sparta_7635d4fb83(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_C]=7;D=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name=_F)
def sparta_6892fe1e7f(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_C]=10;D=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name=_F)
def sparta_43f2120c61(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_C]=11;D=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name=_F)
def sparta_31cfbee9e0(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_2041d0ee11.sparta_680724b699(C,A.user);D=not E[_N]
	if D:return sparta_7635d4fb83(A)
	B=qube_4ed691eaf9.sparta_74b58b0068(A);B[_C]=7;F=qube_4ed691eaf9.sparta_85b2d98a0f(A.user);B.update(F);B[_D]=_A;B[_L]=C;G=E[_H];B[_M]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_993310294e
def sparta_58d13bdf09(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return plot_widget_func(A,B)
@csrf_exempt
@sparta_993310294e
def sparta_50e96b5ad6(request,dashboard_id,id,password):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	C=base64.b64decode(password).decode();return plot_widget_func(A,B,dashboard_id=dashboard_id,dashboard_password=C)
@csrf_exempt
@sparta_993310294e
def sparta_439927e6e2(request,widget_id,session_id,api_token_id):return plot_widget_func(request,widget_id,session_id)
def plot_widget_func(request,plot_chart_id,session=_E,dashboard_id=_E,token_permission='',dashboard_password=_B):
	K='token_permission';I=dashboard_id;H=plot_chart_id;G='res';E=token_permission;D=request;C=_G
	if H is _B:C=_A
	else:
		B=qube_2041d0ee11.sparta_5269a4d561(H,D.user);F=B[G]
		if F==-1:C=_A
	if C:
		if I!=_E:
			B=qube_64734ec0f9.has_plot_db_access(I,H,D.user,dashboard_password);F=B[G]
			if F==1:E=B[K];C=_G
	if C:
		if len(E)>0:
			B=qube_2041d0ee11.sparta_2b7a23741d(E);F=B[G]
			if F==1:C=_G
	if C:return sparta_7635d4fb83(D)
	A=qube_4ed691eaf9.sparta_74b58b0068(D);A[_C]=7;L=qube_4ed691eaf9.sparta_85b2d98a0f(D.user);A.update(L);A[_D]=_A;J=B[_H];A['b_require_password']=0 if B[G]==1 else 1;A[_L]=J.plot_chart_id;A[_M]=J.name;A['session']=str(session);A['is_dashboard_widget']=1 if I!=_E else 0;A['is_token']=1 if len(E)>0 else 0;A[K]=str(E);return render(D,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
def sparta_584f11cc02(request,token):return plot_widget_func(request,plot_chart_id=_B,token_permission=token)
@csrf_exempt
@sparta_993310294e
def sparta_23a027e92a(request):B=request;A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_C]=7;C=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(C);A[_D]=_A;A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_993310294e
@login_required(redirect_field_name=_F)
def sparta_c25b4b6ee4(request,id):
	K=',\n    ';B=request;C=id;F=_G
	if C is _B:F=_A
	else:G=qube_2041d0ee11.sparta_680724b699(C,B.user);F=not G[_N]
	if F:return sparta_7635d4fb83(B)
	L=qube_2041d0ee11.sparta_f3bfcb8e3b(G[_H]);D='';H=0
	for(E,I)in L.items():
		if H>0:D+=K
		if I==1:D+=f"{E}=input_{E}"
		else:M=str(K.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{M}]"
		H+=1
	J=f"'{C}'";N=f"\n    {J}\n";O=f"Spartaqube().get_widget({N})";P=f"\n    {J},\n    {D}\n";Q=f"Spartaqube().plot({P})";A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_C]=7;R=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(R);A[_D]=_A;A[_L]=C;S=G[_H];A[_M]=S.name;A['plot_data_cmd']=O;A['plot_data_cmd_inputs']=Q;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_993310294e
def sparta_3e8fffa04e(request,json_vars_html):B=request;A=qube_4ed691eaf9.sparta_74b58b0068(B);A[_C]=7;C=qube_4ed691eaf9.sparta_85b2d98a0f(B.user);A.update(C);A[_D]=_A;A.update(json.loads(json_vars_html));A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotAPI.html',A)