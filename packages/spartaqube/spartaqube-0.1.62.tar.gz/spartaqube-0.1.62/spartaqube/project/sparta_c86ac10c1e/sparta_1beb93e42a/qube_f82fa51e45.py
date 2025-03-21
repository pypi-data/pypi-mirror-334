_P='is_spartaqube_developer_mode'
_O='json_data'
_N='SET VENV DEVELOPER DEBUG > set_venv_developer'
_M='backend'
_L='kernelManagerUUID'
_K='notebookId'
_J='developerId'
_I=None
_H='dashboardId'
_G='projectPath'
_F='-1'
_E='errorMsg'
_D='env_name'
_C=True
_B=False
_A='res'
import os,sys,subprocess,shutil,getpass,platform,json,base64,zipfile,io,uuid
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
import pytz
UTC=pytz.utc
from project.models_spartaqube import Dashboard,DashboardShared,Developer,DeveloperShared,Notebook,NotebookShared,Kernel,KernelShared
from project.models import ShareRights
from project.sparta_c86ac10c1e.sparta_41804951fe import qube_9ad248f4ee as qube_9ad248f4ee
from project.sparta_c86ac10c1e.sparta_7ef5ced1d2 import qube_edd1fdc02e as qube_edd1fdc02e
from project.sparta_c86ac10c1e.sparta_45f849ee34.qube_9cbbe19431 import sparta_26b96afe1f,sparta_9ff9d23bae
from project.sparta_c86ac10c1e.sparta_45f849ee34.qube_8460cefce9 import sparta_90ad52a9f3
from project.sparta_c86ac10c1e.sparta_d3da874fba import qube_21fd14cf2a as qube_21fd14cf2a
from project.logger_config import logger
def sparta_35acb13806(user_obj):
	A=qube_9ad248f4ee.sparta_ca0a23ce8e(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_12b3bfa3af():B=sparta_90ad52a9f3();A=os.path.join(B,'sq_venv');os.makedirs(A,exist_ok=_C);return A
def sparta_a82ad50ccc(env_name):
	A=env_name;B=sparta_12b3bfa3af()
	if sys.platform=='win32':C=os.path.join(B,A,'Scripts','pip.exe')
	else:C=os.path.join(B,A,'bin','pip')
	return C
def sparta_b86b43302c(json_data,user_obj):A=sparta_12b3bfa3af();B=[B for B in os.listdir(A)if os.path.isdir(os.path.join(A,B))];return{_A:1,'available_venvs':B}
def sparta_29c00f3546(json_data,user_obj):
	B=sparta_12b3bfa3af();A=json_data[_D];C=os.path.join(B,A)
	try:
		subprocess.run([sys.executable,'-m','venv',C],check=_C);D=['cloudpickle']
		for E in D:
			F=sparta_a82ad50ccc(A);G=f"pip install {E}";H=G.replace('pip',F);I=subprocess.Popen(H,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_C)
			for J in I.stdout:logger.debug(J)
		return{_A:1}
	except Exception as K:return{_A:-1,_E:f"Failed to create virtual environment with error {str(K)}"}
def sparta_b920e0e771(json_data,user_obj):
	C=json_data;B=user_obj;F=C[_H];D=Dashboard.objects.filter(dashboard_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.dashboard_id;G=sparta_35acb13806(B)
		if len(G)>0:E=DashboardShared.objects.filter(Q(is_delete=0,user_group__in=G,dashboard__is_delete=0,dashboard=A)|Q(is_delete=0,user=B,dashboard__is_delete=0,dashboard=A))
		else:E=DashboardShared.objects.filter(is_delete=0,user=B,dashboard__is_delete=0,dashboard=A)
		H=_B
		if E.count()>0:
			J=E[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:K=C[_D];A.dashboard_venv=K;A.save()
	L=qube_21fd14cf2a.sparta_239e308861(C,B);return{_A:1}
def sparta_8462467eb1(json_data,user_obj):
	B=user_obj;E=json_data[_H];C=Dashboard.objects.filter(dashboard_id__startswith=E,is_delete=_B).all()
	if C.count()==1:
		A=C[C.count()-1];E=A.dashboard_id;F=sparta_35acb13806(B)
		if len(F)>0:D=DashboardShared.objects.filter(Q(is_delete=0,user_group__in=F,dashboard__is_delete=0,dashboard=A)|Q(is_delete=0,user=B,dashboard__is_delete=0,dashboard=A))
		else:D=DashboardShared.objects.filter(is_delete=0,user=B,dashboard__is_delete=0,dashboard=A)
		G=_B
		if D.count()>0:
			I=D[0];H=I.share_rights
			if H.is_admin or H.has_write_rights:G=_C
		if G:J=_I;A.dashboard_venv=J;A.save()
	return{_A:1}
def sparta_8f78016bd8(json_data,user_obj):
	C=user_obj;A=json_data;D=A[_H];E=A[_J]
	if str(D)!=_F:sparta_8462467eb1(A,C)
	if str(E)!=_F:sparta_9ec72f500f(A,C)
	F=sparta_12b3bfa3af();G=A[_D];H=os.path.join(F,G)
	try:shutil.rmtree(H);return{_A:1}
	except FileNotFoundError as B:return{_A:-1,_E:str(B)}
	except Exception as B:return{_A:-1,_E:str(B)}
def sparta_8370358fa4(json_data,user_obj):
	B=json_data[_D];C=sparta_a82ad50ccc(B);A=[]
	try:
		D=subprocess.run([C,'list'],capture_output=_C,text=_C,check=_C);E=D.stdout.strip().splitlines()[2:]
		for F in E:G,H=F.split()[:2];A.append({'name':G,'version':H})
		return{_A:1,'libraries':A}
	except Exception as I:return{_A:-1,_E:str(I)}
def sparta_ad0f7fd6dd(env_name,project_path):
	A=os.path.join(project_path,'requirements.txt');B=sparta_a82ad50ccc(env_name)
	try:
		with open(A,'w')as C:subprocess.run([B,'freeze'],stdout=C)
		return{_A:1}
	except Exception as D:return{_A:-1,_E:str(D)}
def sparta_0ac60668d4(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug(_N);logger.debug(B);F=B[_J];D=Developer.objects.filter(developer_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.developer_id;G=sparta_35acb13806(C)
		if len(G)>0:E=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=G,developer__is_delete=0,developer=A)|Q(is_delete=0,user=C,developer__is_delete=0,developer=A))
		else:E=DeveloperShared.objects.filter(is_delete=0,user=C,developer__is_delete=0,developer=A)
		H=_B
		if E.count()>0:
			J=E[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:K=B[_D];A.developer_venv=K;A.save()
	L=qube_21fd14cf2a.sparta_239e308861(B,C);return{_A:1}
def sparta_9ec72f500f(json_data,user_obj):
	B=user_obj;E=json_data[_J];C=Developer.objects.filter(developer_id__startswith=E,is_delete=_B).all()
	if C.count()==1:
		A=C[C.count()-1];E=A.developer_id;F=sparta_35acb13806(B)
		if len(F)>0:D=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=F,developer__is_delete=0,developer=A)|Q(is_delete=0,user=B,developer__is_delete=0,developer=A))
		else:D=DeveloperShared.objects.filter(is_delete=0,user=B,developer__is_delete=0,developer=A)
		G=_B
		if D.count()>0:
			I=D[0];H=I.share_rights
			if H.is_admin or H.has_write_rights:G=_C
		if G:J=_I;A.developer_venv=J;A.save()
	return{_A:1}
def sparta_33bf13b09d(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug(_N);logger.debug(B);F=B[_K];D=Notebook.objects.filter(notebook_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.notebook_id;G=sparta_35acb13806(C)
		if len(G)>0:E=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=C,notebook__is_delete=0,notebook=A))
		else:E=NotebookShared.objects.filter(is_delete=0,user=C,notebook__is_delete=0,notebook=A)
		H=_B
		if E.count()>0:
			J=E[0];I=J.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:K=B[_D];A.notebook_venv=K;A.save()
	L=qube_21fd14cf2a.sparta_239e308861(B,C);return{_A:1}
def sparta_9e6d1e4779(json_data,user_obj):
	B=user_obj;E=json_data[_K];C=Notebook.objects.filter(notebook_id__startswith=E,is_delete=_B).all()
	if C.count()==1:
		A=C[C.count()-1];E=A.notebook_id;F=sparta_35acb13806(B)
		if len(F)>0:D=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=F,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=B,notebook__is_delete=0,notebook=A))
		else:D=NotebookShared.objects.filter(is_delete=0,user=B,notebook__is_delete=0,notebook=A)
		G=_B
		if D.count()>0:
			I=D[0];H=I.share_rights
			if H.is_admin or H.has_write_rights:G=_C
		if G:J=_I;A.notebook_venv=J;A.save()
	return{_A:1}
def sparta_31fe71a81c(json_data,user_obj):
	C=json_data;B=user_obj;from project.sparta_c86ac10c1e.sparta_d3da874fba import qube_21fd14cf2a as J;F=C[_L];D=Kernel.objects.filter(kernel_manager_uuid__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.kernel_manager_uuid;G=sparta_35acb13806(B)
		if len(G)>0:E=KernelShared.objects.filter(Q(is_delete=0,user_group__in=G,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=B,kernel__is_delete=0,kernel=A))
		else:E=KernelShared.objects.filter(is_delete=0,user=B,kernel__is_delete=0,kernel=A)
		H=_B
		if E.count()>0:
			K=E[0];I=K.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:L=C[_D];A.kernel_venv=L;A.save()
	M=J.sparta_239e308861(C,B);return{_A:1}
def sparta_fb6be459f4(json_data,user_obj):
	B=user_obj;E=json_data[_L];C=Kernel.objects.filter(kernel_manager_uuid__startswith=E,is_delete=_B).all()
	if C.count()==1:
		A=C[C.count()-1];E=A.kernel_manager_uuid;F=sparta_35acb13806(B)
		if len(F)>0:D=KernelShared.objects.filter(Q(is_delete=0,user_group__in=F,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=B,kernel__is_delete=0,kernel=A))
		else:D=KernelShared.objects.filter(is_delete=0,user=B,kernel__is_delete=0,kernel=A)
		G=_B
		if D.count()>0:
			I=D[0];H=I.share_rights
			if H.is_admin or H.has_write_rights:G=_C
		if G:J=_I;A.kernel_venv=J;A.save()
	return{_A:1}
def sparta_a96939b83e(json_data,user_obj):
	B=user_obj;A=json_data;logger.debug(_O);logger.debug(A);D=A[_H];E=A[_J];F=A[_K];G=A[_L]
	if str(D)!=_F:return sparta_fb88d92c09(A,B)
	if str(E)!=_F:return sparta_cdccc77e4c(A,B)
	if str(F)!=_F:return sparta_e0ce57afc1(A,B)
	if str(G)!=_F:return sparta_faaee67e8c(A,B)
	H=A[_D];C=A[_G]
	if A[_P]:C=os.path.join(C,_M)
	return sparta_ad0f7fd6dd(H,C)
def sparta_fb88d92c09(json_data,user_obj):
	C=user_obj;B=json_data;F=B[_H];J=B[_D];K=B[_G];D=Dashboard.objects.filter(dashboard_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.dashboard_id;G=sparta_35acb13806(C)
		if len(G)>0:E=DashboardShared.objects.filter(Q(is_delete=0,user_group__in=G,dashboard__is_delete=0,dashboard=A)|Q(is_delete=0,user=C,dashboard__is_delete=0,dashboard=A))
		else:E=DashboardShared.objects.filter(is_delete=0,user=C,dashboard__is_delete=0,dashboard=A)
		H=_B
		if E.count()>0:
			L=E[0];I=L.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:return sparta_ad0f7fd6dd(J,K)
	return{_A:1}
def sparta_cdccc77e4c(json_data,user_obj):
	C=user_obj;B=json_data;G=B[_J];K=B[_D];D=B[_G];D=os.path.join(D,_M);E=Developer.objects.filter(developer_id__startswith=G,is_delete=_B).all()
	if E.count()==1:
		A=E[E.count()-1];G=A.developer_id;H=sparta_35acb13806(C)
		if len(H)>0:F=DeveloperShared.objects.filter(Q(is_delete=0,user_group__in=H,developer__is_delete=0,developer=A)|Q(is_delete=0,user=C,developer__is_delete=0,developer=A))
		else:F=DeveloperShared.objects.filter(is_delete=0,user=C,developer__is_delete=0,developer=A)
		I=_B
		if F.count()>0:
			L=F[0];J=L.share_rights
			if J.is_admin or J.has_write_rights:I=_C
		if I:return sparta_ad0f7fd6dd(K,D)
	return{_A:1}
def sparta_e0ce57afc1(json_data,user_obj):
	C=user_obj;B=json_data;F=B[_K];J=B[_D];K=B[_G];D=Notebook.objects.filter(notebook_id__startswith=F,is_delete=_B).all()
	if D.count()==1:
		A=D[D.count()-1];F=A.developer_id;G=sparta_35acb13806(C)
		if len(G)>0:E=NotebookShared.objects.filter(Q(is_delete=0,user_group__in=G,notebook__is_delete=0,notebook=A)|Q(is_delete=0,user=C,notebook__is_delete=0,notebook=A))
		else:E=NotebookShared.objects.filter(is_delete=0,user=C,notebook__is_delete=0,notebook=A)
		H=_B
		if E.count()>0:
			L=E[0];I=L.share_rights
			if I.is_admin or I.has_write_rights:H=_C
		if H:return sparta_ad0f7fd6dd(J,K)
	return{_A:1}
def sparta_faaee67e8c(json_data,user_obj):
	A=json_data;from project.sparta_c86ac10c1e.sparta_d3da874fba import qube_21fd14cf2a as B;C=A[_L];D=A[_D];E=A[_G];F=B.sparta_b14df55eaa(user_obj,C)
	if F is _I:return sparta_ad0f7fd6dd(D,E)
	return{_A:1}
def sparta_39becda479(json_data,user_obj):
	B=json_data;logger.debug(_O);logger.debug(B);E=B[_D];C=os.path.join(sparta_12b3bfa3af(),E);logger.debug('venv_path');logger.debug(C);A=sparta_26b96afe1f(B[_G])
	if B[_P]:A=os.path.join(A,_M)
	if not os.path.isdir(A):return{_A:-1,_E:f"The provided path '{A}' is not a valid directory."}
	D=platform.system()
	try:
		if D=='Windows':os.system(f'start cmd /K "cd /d {A} && {C}\\Scripts\\activate.bat"')
		elif D=='Linux':subprocess.run(['x-terminal-emulator','-e',f'bash -c "cd {A} && source {C}/bin/activate && exec bash"'],check=_C)
		elif D=='Darwin':F=f'''
            tell application "Terminal"
                do script "cd {A} && source {C}/bin/activate"
                activate
            end tell
            ''';subprocess.run(['osascript','-e',F],check=_C)
		else:return{_A:-1,_E:'Unsupported operating system.'}
	except Exception as G:return{_A:-1,_E:f"Failed to open terminal and activate venv at '{A}': {G}"}
	return{_A:1}