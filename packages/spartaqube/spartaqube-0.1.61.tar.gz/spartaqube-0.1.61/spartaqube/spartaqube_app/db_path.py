import os,sys,getpass,platform
from project.sparta_aac227c3fb.sparta_e0ad6143e8.qube_533d926758 import sparta_978905e1c8,sparta_9e0a9d0db9
def sparta_5aff052fbd(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_f3ea7f9d0f():
	if sparta_9e0a9d0db9():A='/app/APPDATA/local_db/db.sqlite3'
	else:C=sparta_978905e1c8();B=os.path.join(C,'data');sparta_5aff052fbd(B);A=os.path.join(B,'db.sqlite3')
	return A