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
from project.sparta_aac227c3fb.sparta_b3647f8030.qube_b5aadfcc12 import sparta_508aabc108,sparta_8fa5310cbe,sparta_ccaa977401
from project.sparta_aac227c3fb.sparta_27abf0b36c.qube_2e0ebaa5c3 import SenderKernel
from project.logger_config import logger
def sparta_16d8fd301f():
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as A:A.bind(('',0));return A.getsockname()[1]
class SqKernelManager:
	def __init__(A,kernel_manager_uuid,type,name,user,user_kernel=_A,project_folder=_A,notebook_exec_id=_E,dashboard_exec_id=_E,venv_name=_A):
		C=user_kernel;B=user;A.kernel_manager_uuid=kernel_manager_uuid;A.type=type;A.name=name;A.user=B;A.kernel_user_logged=B;A.project_folder=project_folder
		if C is _A:C=B
		A.user_kernel=C;A.venv_name=venv_name;A.notebook_exec_id=notebook_exec_id;A.dashboard_exec_id=dashboard_exec_id;A.is_init=_F;A.created_time=datetime.now()
	def create_kernel(A,django_settings_module=_A):
		if A.notebook_exec_id!=_E:A.user_kernel=sparta_8fa5310cbe(A.notebook_exec_id)
		if A.dashboard_exec_id!=_E:A.user_kernel=sparta_ccaa977401(A.dashboard_exec_id)
		G=os.path.dirname(__file__);H=sparta_508aabc108(A.user_kernel);C=sparta_16d8fd301f();I=sys.executable;J=A.venv_name if A.venv_name is not _A else _E
		def L(pipe):
			for A in iter(pipe.readline,''):logger.debug(A,end='')
			pipe.close()
		E=os.environ.copy();E['ZMQ_PROCESS']='1';logger.debug(f"SPAWN PYTHON KERNEL {C}");K=subprocess.Popen([I,_L,str(H),str(C),J],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_D,cwd=G,env=E);F=K.pid;D=datetime.now().astimezone(UTC);B=sparta_4f7a5a6d1f(A.user,A.kernel_manager_uuid)
		if B is _A:B=KernelProcess.objects.create(kernel_manager_uuid=A.kernel_manager_uuid,port=C,pid=F,date_created=D,user=A.user,name=A.name,type=A.type,notebook_exec_id=A.notebook_exec_id,dashboard_exec_id=A.dashboard_exec_id,venv_name=A.venv_name,project_folder=A.project_folder,last_update=D)
		else:B.port=C;B.pid=F;B.name=A.name;B.type=A.type;B.notebook_exec_id=A.notebook_exec_id;B.dashboard_exec_id=A.dashboard_exec_id;B.venv_name=A.venv_name;B.project_folder=A.project_folder;B.last_update=D;B.save()
		return{_B:1,_M:B}
def sparta_20d62e0306(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_size()
def sparta_0171938567(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_workspace_variables()
def sparta_fa02fa1d5a(kernel_process_obj,venv_name):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_activate_venv(venv_name)
def sparta_b228dca7ed(kernel_process_obj,kernel_varname):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_variable_repr(kernel_varname)
def sparta_eeb2c6430b(kernel_process_obj,var_name,var_value):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_set_workspace_variable(var_name,var_value)
def set_workspace_cloudpickle_variables(kernel_process_obj,cloudpickle_kernel_variables):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_set_workspace_cloudpickle_variables(cloudpickle_kernel_variables)
def sparta_d18a099107(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_cloudpickle_kernel_variables()
def sparta_4dc10b4d69(pid):
	logger.debug('Force Kill Process now from kernel manager')
	if platform.system()==_N:return sparta_e4dd729221(pid)
	else:return sparta_b6f53a2e64(pid)
def sparta_e4dd729221(pid):
	try:subprocess.run(['taskkill','/F','/PID',str(pid)],check=_D,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError:logger.debug(f"Failed to kill process {pid}. It may not exist.")
def sparta_b6f53a2e64(pid):
	try:subprocess.run(['kill','-9',str(pid)],check=_D,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError:logger.debug(f"Failed to kill process {pid}. It may not exist.")
def sparta_f40a93fba1(kernel_process_obj):A=kernel_process_obj.pid;sparta_4dc10b4d69(A)
def sparta_4f7a5a6d1f(user_obj,kernel_manager_uuid):
	A=KernelProcess.objects.filter(user=user_obj,kernel_manager_uuid=kernel_manager_uuid,is_delete=_F)
	if A.count()>0:return A[0]
def sparta_245a5dcec7(json_data,user_obj,b_return_model=_F):
	E=user_obj;A=json_data;logger.debug('Create new kernel');logger.debug(A);H=A[_C];B=int(A[_O]);I=A.get(_G,'undefined');C=A.get('fullpath',_A);J=A.get('notebookExecId',_E);K=A.get('dashboardExecId',_E);D=A.get(_P,'')
	if len(D)==0:D=_A
	if C is not _A:C=os.path.dirname(C)
	F=SqKernelManager(H,B,I,E,user_kernel=E,project_folder=C,notebook_exec_id=J,dashboard_exec_id=K,venv_name=D)
	if B==3 or B==4 or B==5:G=F.create_kernel(django_settings_module=_Q)
	else:G=F.create_kernel()
	if b_return_model:return G
	return{_B:1}
def sparta_bad704a44f(json_data,user_obj):
	C=user_obj;D=json_data[_C];A=sparta_4f7a5a6d1f(C,D)
	if A is not _A:
		sparta_f40a93fba1(A);B=A.type;F=A.name;G=A.project_folder;H=A.notebook_exec_id;I=A.dashboard_exec_id;J=A.user_kernel;K=A.venv_name;E=SqKernelManager(D,B,F,C,user_kernel=J,project_folder=G,notebook_exec_id=H,dashboard_exec_id=I,venv_name=K)
		if B==3 or B==4 or B==5:E.create_kernel(django_settings_module=_Q)
		else:E.create_kernel()
	return{_B:1}
def sparta_6176601ad1(json_data,user_obj):
	A=json_data
	if _C in A:
		C=A[_C];D=A['env_name'];B=sparta_4f7a5a6d1f(user_obj,C)
		if B is not _A:sparta_fa02fa1d5a(B,D)
	return{_B:1}
def sparta_003ccd9fd0(json_data,user_obj):
	B=json_data[_C];A=sparta_4f7a5a6d1f(user_obj,B)
	if A is not _A:C=sparta_20d62e0306(A);D=sparta_0171938567(A);return{_B:1,'kernel':{_R:D,_H:B,'kernel_size':C,'type':A.type,_G:A.name,_S:str(A.date_created.strftime(_U)),_T:naturalday(parser.parse(str(A.date_created)))}}
	return{_B:-1}
def sparta_029b9f8116(json_data,user_obj):
	A=json_data;C=A[_C];D=A['varName'];B=sparta_4f7a5a6d1f(user_obj,C)
	if B is not _A:E=sparta_b228dca7ed(B,D);return{_B:1,'htmlReprDict':E}
	return{_B:-1}
def sparta_34e78fd131(json_data,user_obj):
	C=json_data;D=C[_C];A=sparta_4f7a5a6d1f(user_obj,D)
	if A is not _A:
		B=C.get(_G,_A)
		if B is not _A:A.name=B;A.save();sparta_eeb2c6430b(A,_G,B)
	return{_B:1}
def sparta_107aee9626():
	if platform.system()==_N:return sparta_452fc84a65()
	else:return sparta_ec2e4d7801()
def sparta_942eca32de(command):
	with concurrent.futures.ThreadPoolExecutor()as A:B=A.submit(subprocess.run,command,shell=_D,capture_output=_D,text=_D);C=B.result();return C.stdout.strip()
def sparta_452fc84a65():
	try:
		E='wmic process where "name=\'python.exe\'" get ProcessId,ParentProcessId,CommandLine /FORMAT:CSV';F=sparta_942eca32de(E);C=[];G=F.splitlines()
		for H in G[2:]:
			A=[A.strip()for A in H.split(',')]
			if len(A)<4:continue
			B=A[1];I=A[2];J=A[3]
			if _L in B:D=B.split();K=D[3]if len(D)>3 else _A;C.append({'PID':I,_I:J,_V:B,_J:K})
		return C
	except Exception as L:logger.error(f"Unexpected error finding spawnKernel.py: {L}");return[]
def sparta_ec2e4d7801():
	try:
		E=sparta_942eca32de("ps -eo pid,ppid,command | grep '[s]pawnKernel.py'");A=[];F=E.split('\n')
		for G in F:
			B=G.strip().split(maxsplit=2)
			if len(B)<3:continue
			H,I,C=B;D=C.split();J=D[3]if len(D)>3 else _A;A.append({'PID':H,_I:I,_V:C,_J:J})
		return A
	except Exception as K:logger.error(f"Unexpected error finding spawnKernel.py: {K}");return[]
def sparta_5aa530bff0(json_data,user_obj):
	I='b_require_workspace_variables';C=user_obj;B=json_data;J=B.get('b_require_size',_F);K=B.get(I,_F);L=B.get(I,_F);D=[]
	if L:from project.sparta_aac227c3fb.sparta_9a5153ccce import qube_0f3817b689 as M;D=M.sparta_99ba9566ca(C)
	N=sparta_107aee9626();E=[(A[_I],A[_J])for A in N];O=KernelProcess.objects.filter(pid__in=[A[0]for A in E],port__in=[A[1]for A in E],user=C).distinct();F=[]
	for A in O:
		G=_A
		if J:G=sparta_20d62e0306(A)
		H=[]
		if K:H=sparta_0171938567(A)
		F.append({_H:A.kernel_manager_uuid,_R:H,'type':A.type,_G:A.name,_S:str(A.date_created.strftime(_U)),_T:naturalday(parser.parse(str(A.date_created))),'size':G,'isStored':_D if A.kernel_manager_uuid in D else _F})
	return{_B:1,_K:F}
def sparta_2fbcb259e2(json_data,user_obj):
	B=user_obj;from project.sparta_aac227c3fb.sparta_9a5153ccce import qube_0f3817b689 as D;A=D.sparta_eaf8883268(B);C=sparta_5aa530bff0(json_data,B)
	if C[_B]==1:E=C[_K];F=[A[_H]for A in E];A=[A for A in A if A[_H]not in F];return{_B:1,'kernel_library':A}
	return{_B:-1}
def sparta_0bd29ad0c6(json_data,user_obj):
	B=json_data[_C];A=sparta_4f7a5a6d1f(user_obj,B)
	if A is not _A:sparta_f40a93fba1(A)
	return{_B:1}
def sparta_fa60caa336(json_data,user_obj):
	A=user_obj;B=sparta_5aa530bff0(json_data,A)
	if B[_B]==1:
		C=B[_K]
		for D in C:E={_C:D[_H]};sparta_0bd29ad0c6(E,A)
	return{_B:1}
def sparta_e558cf6509(json_data,user_obj):
	C=user_obj;B=json_data;D=B[_C];from project.sparta_aac227c3fb.sparta_9a5153ccce import qube_0f3817b689 as I;G=I.sparta_ff278c65c6(C,D);A=sparta_4f7a5a6d1f(C,D)
	if A is not _A:
		E=A.venv_name
		if E is _A:E=''
		B={_O:100,_C:D,_G:A.name,_P:E};F=sparta_245a5dcec7(B,C,_D)
		if F[_B]==1:
			A=F[_M]
			if G.is_static_variables:
				H=G.kernel_variables
				if H is not _A:set_workspace_cloudpickle_variables(A,H)
		return{_B:F[_B]}
	return{_B:-1}
def sparta_66955c355d(json_data,user_obj):return{_B:1}