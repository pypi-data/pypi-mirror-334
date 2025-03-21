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
import project.sparta_3d2a895074.sparta_28819454f8.qube_05f3410cc3 as qube_05f3410cc3
from project.sparta_c86ac10c1e.sparta_e6b12a1d61.qube_b0ec55220f import sparta_cbd160ca6d
from project.sparta_c86ac10c1e.sparta_d3a4fd1e04 import qube_af72c7c492 as qube_af72c7c492
from project.sparta_c86ac10c1e.sparta_433a8e7b64 import qube_4ec6b7e2b1 as qube_4ec6b7e2b1
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name=_F)
def sparta_c5310aa93c(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_C]=7;D=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name=_F)
def sparta_c16ff99e05(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_C]=10;D=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name=_F)
def sparta_9c13119867(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_05f3410cc3.sparta_40b78ff765(B);A[_C]=11;D=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name=_F)
def sparta_234df7bc4d(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_af72c7c492.sparta_ced2f3469d(C,A.user);D=not E[_N]
	if D:return sparta_c5310aa93c(A)
	B=qube_05f3410cc3.sparta_40b78ff765(A);B[_C]=7;F=qube_05f3410cc3.sparta_7e34f10c40(A.user);B.update(F);B[_D]=_A;B[_L]=C;G=E[_H];B[_M]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_cbd160ca6d
def sparta_9c57428151(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return plot_widget_func(A,B)
@csrf_exempt
@sparta_cbd160ca6d
def sparta_37ed07ae5d(request,dashboard_id,id,password):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	C=base64.b64decode(password).decode();return plot_widget_func(A,B,dashboard_id=dashboard_id,dashboard_password=C)
@csrf_exempt
@sparta_cbd160ca6d
def sparta_d125ee5386(request,widget_id,session_id,api_token_id):return plot_widget_func(request,widget_id,session_id)
def plot_widget_func(request,plot_chart_id,session=_E,dashboard_id=_E,token_permission='',dashboard_password=_B):
	K='token_permission';I=dashboard_id;H=plot_chart_id;G='res';E=token_permission;D=request;C=_G
	if H is _B:C=_A
	else:
		B=qube_af72c7c492.sparta_270d2b65c2(H,D.user);F=B[G]
		if F==-1:C=_A
	if C:
		if I!=_E:
			B=qube_4ec6b7e2b1.has_plot_db_access(I,H,D.user,dashboard_password);F=B[G]
			if F==1:E=B[K];C=_G
	if C:
		if len(E)>0:
			B=qube_af72c7c492.sparta_45bf929069(E);F=B[G]
			if F==1:C=_G
	if C:return sparta_c5310aa93c(D)
	A=qube_05f3410cc3.sparta_40b78ff765(D);A[_C]=7;L=qube_05f3410cc3.sparta_7e34f10c40(D.user);A.update(L);A[_D]=_A;J=B[_H];A['b_require_password']=0 if B[G]==1 else 1;A[_L]=J.plot_chart_id;A[_M]=J.name;A['session']=str(session);A['is_dashboard_widget']=1 if I!=_E else 0;A['is_token']=1 if len(E)>0 else 0;A[K]=str(E);return render(D,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
def sparta_b20d447936(request,token):return plot_widget_func(request,plot_chart_id=_B,token_permission=token)
@csrf_exempt
@sparta_cbd160ca6d
def sparta_9518306a47(request):B=request;A=qube_05f3410cc3.sparta_40b78ff765(B);A[_C]=7;C=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(C);A[_D]=_A;A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_cbd160ca6d
@login_required(redirect_field_name=_F)
def sparta_ee61643ed7(request,id):
	K=',\n    ';B=request;C=id;F=_G
	if C is _B:F=_A
	else:G=qube_af72c7c492.sparta_ced2f3469d(C,B.user);F=not G[_N]
	if F:return sparta_c5310aa93c(B)
	L=qube_af72c7c492.sparta_835f92cb3f(G[_H]);D='';H=0
	for(E,I)in L.items():
		if H>0:D+=K
		if I==1:D+=f"{E}=input_{E}"
		else:M=str(K.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{M}]"
		H+=1
	J=f"'{C}'";N=f"\n    {J}\n";O=f"Spartaqube().get_widget({N})";P=f"\n    {J},\n    {D}\n";Q=f"Spartaqube().plot({P})";A=qube_05f3410cc3.sparta_40b78ff765(B);A[_C]=7;R=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(R);A[_D]=_A;A[_L]=C;S=G[_H];A[_M]=S.name;A['plot_data_cmd']=O;A['plot_data_cmd_inputs']=Q;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_cbd160ca6d
def sparta_7bb6f8977e(request,json_vars_html):B=request;A=qube_05f3410cc3.sparta_40b78ff765(B);A[_C]=7;C=qube_05f3410cc3.sparta_7e34f10c40(B.user);A.update(C);A[_D]=_A;A.update(json.loads(json_vars_html));A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotAPI.html',A)