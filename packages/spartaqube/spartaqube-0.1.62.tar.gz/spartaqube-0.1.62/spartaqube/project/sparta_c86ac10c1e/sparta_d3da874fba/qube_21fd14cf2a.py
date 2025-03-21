_V='CommandLine'
_U='%Y-%m-%d %H:%M:%S'
_T='created_time'
_S='created_time_str'
_R='workspace_variables'
_Q='app.settings'
_P='venvName'
_O='kernelType'
_N='Windows'
_M='kernel_process_obj'
_L='spawnKernel.py'
_K='kernels'
_J='port'
_I='PPID'
_H='kernel_manager_uuid'
_G='name'
_F=False
_E='-1'
_D=True
_C='kernelManagerUUID'
_B='res'
_A=None
import os,sys,gc,socket,subprocess,threading,platform,psutil,zmq,json,base64,shutil,zipfile,io,uuid,cloudpickle
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC=pytz.utc
import concurrent.futures
from django.contrib.humanize.templatetags.humanize import naturalday
from project.models import KernelProcess
from project.sparta_c86ac10c1e.sparta_ec46e9a9b4.qube_6e3dd19911 import sparta_9de5364c58,sparta_48b142384b,sparta_826709597e
from project.sparta_c86ac10c1e.sparta_d3da874fba.qube_581111b792 import SenderKernel
from project.logger_config import logger
def sparta_a0ebb35978():
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as A:A.bind(('',0));return A.getsockname()[1]
class SqKernelManager:
	def __init__(A,kernel_manager_uuid,type,name,user,user_kernel=_A,project_folder=_A,notebook_exec_id=_E,dashboard_exec_id=_E,venv_name=_A):
		C=user_kernel;B=user;A.kernel_manager_uuid=kernel_manager_uuid;A.type=type;A.name=name;A.user=B;A.kernel_user_logged=B;A.project_folder=project_folder
		if C is _A:C=B
		A.user_kernel=C;A.venv_name=venv_name;A.notebook_exec_id=notebook_exec_id;A.dashboard_exec_id=dashboard_exec_id;A.is_init=_F;A.created_time=datetime.now()
	def create_kernel(A,django_settings_module=_A):
		if A.notebook_exec_id!=_E:A.user_kernel=sparta_48b142384b(A.notebook_exec_id)
		if A.dashboard_exec_id!=_E:A.user_kernel=sparta_826709597e(A.dashboard_exec_id)
		G=os.path.dirname(__file__);H=sparta_9de5364c58(A.user_kernel);C=sparta_a0ebb35978();I=sys.executable;J=A.venv_name if A.venv_name is not _A else _E
		def L(pipe):
			for A in iter(pipe.readline,''):logger.debug(A,end='')
			pipe.close()
		E=os.environ.copy();E['ZMQ_PROCESS']='1';logger.debug(f"SPAWN PYTHON KERNEL {C}");K=subprocess.Popen([I,_L,str(H),str(C),J],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_D,cwd=G,env=E);F=K.pid;D=datetime.now().astimezone(UTC);B=sparta_b14df55eaa(A.user,A.kernel_manager_uuid)
		if B is _A:B=KernelProcess.objects.create(kernel_manager_uuid=A.kernel_manager_uuid,port=C,pid=F,date_created=D,user=A.user,name=A.name,type=A.type,notebook_exec_id=A.notebook_exec_id,dashboard_exec_id=A.dashboard_exec_id,venv_name=A.venv_name,project_folder=A.project_folder,last_update=D)
		else:B.port=C;B.pid=F;B.name=A.name;B.type=A.type;B.notebook_exec_id=A.notebook_exec_id;B.dashboard_exec_id=A.dashboard_exec_id;B.venv_name=A.venv_name;B.project_folder=A.project_folder;B.last_update=D;B.save()
		return{_B:1,_M:B}
def sparta_fd9d3b320f(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_size()
def sparta_87ef7b5f20(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_workspace_variables()
def sparta_74bf472387(kernel_process_obj,venv_name):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_activate_venv(venv_name)
def sparta_2fc0d012ed(kernel_process_obj,kernel_varname):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_variable_repr(kernel_varname)
def sparta_37935dfde1(kernel_process_obj,var_name,var_value):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_set_workspace_variable(var_name,var_value)
def set_workspace_cloudpickle_variables(kernel_process_obj,cloudpickle_kernel_variables):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_set_workspace_cloudpickle_variables(cloudpickle_kernel_variables)
def sparta_87e6ccc231(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_cloudpickle_kernel_variables()
def sparta_8a448c2af6(pid):
	logger.debug('Force Kill Process now from kernel manager')
	if platform.system()==_N:return sparta_4b10c13fd5(pid)
	else:return sparta_0d423568c7(pid)
def sparta_4b10c13fd5(pid):
	try:subprocess.run(['taskkill','/F','/PID',str(pid)],check=_D,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError:logger.debug(f"Failed to kill process {pid}. It may not exist.")
def sparta_0d423568c7(pid):
	try:subprocess.run(['kill','-9',str(pid)],check=_D,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError:logger.debug(f"Failed to kill process {pid}. It may not exist.")
def sparta_901f988e95(kernel_process_obj):A=kernel_process_obj.pid;sparta_8a448c2af6(A)
def sparta_b14df55eaa(user_obj,kernel_manager_uuid):
	A=KernelProcess.objects.filter(user=user_obj,kernel_manager_uuid=kernel_manager_uuid,is_delete=_F)
	if A.count()>0:return A[0]
def sparta_9ea4b05fa9(json_data,user_obj,b_return_model=_F):
	E=user_obj;A=json_data;logger.debug('Create new kernel');logger.debug(A);H=A[_C];B=int(A[_O]);I=A.get(_G,'undefined');C=A.get('fullpath',_A);J=A.get('notebookExecId',_E);K=A.get('dashboardExecId',_E);D=A.get(_P,'')
	if len(D)==0:D=_A
	if C is not _A:C=os.path.dirname(C)
	F=SqKernelManager(H,B,I,E,user_kernel=E,project_folder=C,notebook_exec_id=J,dashboard_exec_id=K,venv_name=D)
	if B==3 or B==4 or B==5:G=F.create_kernel(django_settings_module=_Q)
	else:G=F.create_kernel()
	if b_return_model:return G
	return{_B:1}
def sparta_376798a87b(json_data,user_obj):
	C=user_obj;D=json_data[_C];A=sparta_b14df55eaa(C,D)
	if A is not _A:
		sparta_901f988e95(A);B=A.type;F=A.name;G=A.project_folder;H=A.notebook_exec_id;I=A.dashboard_exec_id;J=A.user_kernel;K=A.venv_name;E=SqKernelManager(D,B,F,C,user_kernel=J,project_folder=G,notebook_exec_id=H,dashboard_exec_id=I,venv_name=K)
		if B==3 or B==4 or B==5:E.create_kernel(django_settings_module=_Q)
		else:E.create_kernel()
	return{_B:1}
def sparta_239e308861(json_data,user_obj):
	A=json_data
	if _C in A:
		C=A[_C];D=A['env_name'];B=sparta_b14df55eaa(user_obj,C)
		if B is not _A:sparta_74bf472387(B,D)
	return{_B:1}
def sparta_c4f03057c5(json_data,user_obj):
	B=json_data[_C];A=sparta_b14df55eaa(user_obj,B)
	if A is not _A:C=sparta_fd9d3b320f(A);D=sparta_87ef7b5f20(A);return{_B:1,'kernel':{_R:D,_H:B,'kernel_size':C,'type':A.type,_G:A.name,_S:str(A.date_created.strftime(_U)),_T:naturalday(parser.parse(str(A.date_created)))}}
	return{_B:-1}
def sparta_1a31f8ed6b(json_data,user_obj):
	A=json_data;C=A[_C];D=A['varName'];B=sparta_b14df55eaa(user_obj,C)
	if B is not _A:E=sparta_2fc0d012ed(B,D);return{_B:1,'htmlReprDict':E}
	return{_B:-1}
def sparta_cd8627180a(json_data,user_obj):
	C=json_data;D=C[_C];A=sparta_b14df55eaa(user_obj,D)
	if A is not _A:
		B=C.get(_G,_A)
		if B is not _A:A.name=B;A.save();sparta_37935dfde1(A,_G,B)
	return{_B:1}
def sparta_e976e70113():
	if platform.system()==_N:return sparta_1c0c1701d1()
	else:return sparta_8bcfcd54bb()
def sparta_c068805121(command):
	with concurrent.futures.ThreadPoolExecutor()as A:B=A.submit(subprocess.run,command,shell=_D,capture_output=_D,text=_D);C=B.result();return C.stdout.strip()
def sparta_1c0c1701d1():
	try:
		E='wmic process where "name=\'python.exe\'" get ProcessId,ParentProcessId,CommandLine /FORMAT:CSV';F=sparta_c068805121(E);C=[];G=F.splitlines()
		for H in G[2:]:
			A=[A.strip()for A in H.split(',')]
			if len(A)<4:continue
			B=A[1];I=A[2];J=A[3]
			if _L in B:D=B.split();K=D[3]if len(D)>3 else _A;C.append({'PID':I,_I:J,_V:B,_J:K})
		return C
	except Exception as L:logger.error(f"Unexpected error finding spawnKernel.py: {L}");return[]
def sparta_8bcfcd54bb():
	try:
		E=sparta_c068805121("ps -eo pid,ppid,command | grep '[s]pawnKernel.py'");A=[];F=E.split('\n')
		for G in F:
			B=G.strip().split(maxsplit=2)
			if len(B)<3:continue
			H,I,C=B;D=C.split();J=D[3]if len(D)>3 else _A;A.append({'PID':H,_I:I,_V:C,_J:J})
		return A
	except Exception as K:logger.error(f"Unexpected error finding spawnKernel.py: {K}");return[]
def sparta_58d0d47920(json_data,user_obj):
	I='b_require_workspace_variables';C=user_obj;B=json_data;J=B.get('b_require_size',_F);K=B.get(I,_F);L=B.get(I,_F);D=[]
	if L:from project.sparta_c86ac10c1e.sparta_f1e2e6fc12 import qube_34e04aab67 as M;D=M.sparta_000c107bda(C)
	N=sparta_e976e70113();E=[(A[_I],A[_J])for A in N];O=KernelProcess.objects.filter(pid__in=[A[0]for A in E],port__in=[A[1]for A in E],user=C).distinct();F=[]
	for A in O:
		G=_A
		if J:G=sparta_fd9d3b320f(A)
		H=[]
		if K:H=sparta_87ef7b5f20(A)
		F.append({_H:A.kernel_manager_uuid,_R:H,'type':A.type,_G:A.name,_S:str(A.date_created.strftime(_U)),_T:naturalday(parser.parse(str(A.date_created))),'size':G,'isStored':_D if A.kernel_manager_uuid in D else _F})
	return{_B:1,_K:F}
def sparta_81ff0628ff(json_data,user_obj):
	B=user_obj;from project.sparta_c86ac10c1e.sparta_f1e2e6fc12 import qube_34e04aab67 as D;A=D.sparta_96d2946202(B);C=sparta_58d0d47920(json_data,B)
	if C[_B]==1:E=C[_K];F=[A[_H]for A in E];A=[A for A in A if A[_H]not in F];return{_B:1,'kernel_library':A}
	return{_B:-1}
def sparta_1182ed5f49(json_data,user_obj):
	B=json_data[_C];A=sparta_b14df55eaa(user_obj,B)
	if A is not _A:sparta_901f988e95(A)
	return{_B:1}
def sparta_cea373b6e8(json_data,user_obj):
	A=user_obj;B=sparta_58d0d47920(json_data,A)
	if B[_B]==1:
		C=B[_K]
		for D in C:E={_C:D[_H]};sparta_1182ed5f49(E,A)
	return{_B:1}
def sparta_81cafe01e5(json_data,user_obj):
	C=user_obj;B=json_data;D=B[_C];from project.sparta_c86ac10c1e.sparta_f1e2e6fc12 import qube_34e04aab67 as I;G=I.sparta_4b736b8ad2(C,D);A=sparta_b14df55eaa(C,D)
	if A is not _A:
		E=A.venv_name
		if E is _A:E=''
		B={_O:100,_C:D,_G:A.name,_P:E};F=sparta_9ea4b05fa9(B,C,_D)
		if F[_B]==1:
			A=F[_M]
			if G.is_static_variables:
				H=G.kernel_variables
				if H is not _A:set_workspace_cloudpickle_variables(A,H)
		return{_B:F[_B]}
	return{_B:-1}
def sparta_6d78d6a984(json_data,user_obj):return{_B:1}