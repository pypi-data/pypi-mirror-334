_H='execution_count'
_G='cell_type'
_F='code'
_E='outputs'
_D='source'
_C='cells'
_B='sqMetadata'
_A='metadata'
import os,re,uuid,json
from datetime import datetime
from nbconvert.filters import strip_ansi
from project.sparta_c86ac10c1e.sparta_d499b185b8 import qube_95cf9a0554 as qube_95cf9a0554
from project.sparta_c86ac10c1e.sparta_45f849ee34.qube_9cbbe19431 import sparta_26b96afe1f,sparta_9ff9d23bae
from project.logger_config import logger
def sparta_faa63a1b50(file_path):return os.path.isfile(file_path)
def sparta_3fc13901c7():return qube_95cf9a0554.sparta_f0f4ef6dc9(json.dumps({'date':str(datetime.now())}))
def sparta_a7ce34c049():B='python';A='name';C={'kernelspec':{'display_name':'Python 3 (ipykernel)','language':B,A:'python3'},'language_info':{'codemirror_mode':{A:'ipython','version':3},'file_extension':'.py','mimetype':'text/x-python',A:B,'nbconvert_exporter':B,'pygments_lexer':'ipython3'},_B:sparta_3fc13901c7()};return C
def sparta_12b5d788b1():return{_G:_F,_D:[''],_A:{},_H:None,_E:[]}
def sparta_b30a03c6c3():return[sparta_12b5d788b1()]
def sparta_96eaa63c2f():return{'nbformat':4,'nbformat_minor':0,_A:sparta_a7ce34c049(),_C:[]}
def sparta_5e7d7b354c(first_cell_code=''):A=sparta_96eaa63c2f();B=sparta_12b5d788b1();B[_D]=[first_cell_code];A[_C]=[B];return A
def sparta_a3b4b50d18(full_path):
	A=full_path
	if sparta_faa63a1b50(A):return sparta_cd61c95f82(A)
	else:return sparta_5e7d7b354c()
def sparta_cd61c95f82(full_path):return sparta_8ce3eabe3f(full_path)
def sparta_87c99149eb():A=sparta_96eaa63c2f();B=json.loads(qube_95cf9a0554.sparta_e67769de2a(A[_A][_B]));A[_A][_B]=B;return A
def sparta_8ce3eabe3f(full_path):
	with open(full_path)as C:B=C.read()
	if len(B)==0:A=sparta_96eaa63c2f()
	else:A=json.loads(B)
	A=sparta_057edb49cf(A);return A
def sparta_057edb49cf(ipynb_dict):
	A=ipynb_dict;C=list(A.keys())
	if _C in C:
		D=A[_C]
		for B in D:
			if _A in list(B.keys()):
				if _B in B[_A]:B[_A][_B]=qube_95cf9a0554.sparta_e67769de2a(B[_A][_B])
	try:A[_A][_B]=json.loads(qube_95cf9a0554.sparta_e67769de2a(A[_A][_B]))
	except:A[_A][_B]=json.loads(qube_95cf9a0554.sparta_e67769de2a(sparta_3fc13901c7()))
	return A
def sparta_9f41bde041(full_path):
	B=full_path;A=dict()
	with open(B)as C:A=C.read()
	if len(A)==0:A=sparta_87c99149eb();A[_A][_B]=json.dumps(A[_A][_B])
	else:
		A=json.loads(A)
		if _A in list(A.keys()):
			if _B in list(A[_A].keys()):A=sparta_057edb49cf(A);A[_A][_B]=json.dumps(A[_A][_B])
	A['fullPath']=B;return A
def save_ipnyb_from_notebook_cells(notebook_cells_arr,full_path,dashboard_id='-1'):
	R='output_type';Q='markdown';L=full_path;K='tmp_idx';B=[]
	for A in notebook_cells_arr:
		A['bIsComputing']=False;S=A['bDelete'];F=A['cellType'];M=A[_F];T=A['positionIndex'];A[_D]=[M];G=A.get('ipynbOutput',[]);C=A.get('ipynbError',[]);logger.debug('ipynb_output_list');logger.debug(G);logger.debug(type(G));logger.debug('ipynb_error_list');logger.debug(C);logger.debug(type(C));logger.debug('this_cell_dict');logger.debug(A)
		if int(S)==0:
			if F==0:H=_F
			elif F==1:H=Q
			elif F==2:H=Q
			elif F==3:H='raw'
			D={_A:{_B:qube_95cf9a0554.sparta_f0f4ef6dc9(json.dumps(A))},'id':uuid.uuid4().hex[:8],_G:H,_D:[M],_H:None,K:T,_E:[]}
			if len(G)>0:
				N=[]
				for E in G:O={};O[E['type']]=[E['output']];N.append({'data':O,R:'execute_result'})
				D[_E]=N
			elif len(C)>0:
				D[_E]=C
				try:
					J=[];U=re.compile('<ipython-input-\\d+-[0-9a-f]+>')
					for E in C:E[R]='error';J+=[re.sub(U,'<IPY-INPUT>',strip_ansi(A))for A in E['traceback']]
					if len(J)>0:D['tbErrors']='\n'.join(J)
				except Exception as V:logger.debug('Except prepare error output traceback with msg:');logger.debug(V)
			else:D[_E]=[]
			B.append(D)
	B=sorted(B,key=lambda d:d[K]);[A.pop(K,None)for A in B];I=sparta_a3b4b50d18(L);P=I[_A][_B];P['identifier']={'dashboardId':dashboard_id};I[_A][_B]=qube_95cf9a0554.sparta_f0f4ef6dc9(json.dumps(P));I[_C]=B
	with open(L,'w')as W:json.dump(I,W,indent=4)
	return{'res':1}
def sparta_34c191230e(full_path):
	A=full_path;A=sparta_26b96afe1f(A);C=dict()
	with open(A)as D:E=D.read();C=json.loads(E)
	F=C[_C];B=[]
	for G in F:B.append({_F:G[_D][0]})
	logger.debug('notebook_cells_list');logger.debug(B);return B