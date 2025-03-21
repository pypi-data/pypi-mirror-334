import os,sys,getpass,platform
from project.sparta_c86ac10c1e.sparta_45f849ee34.qube_8460cefce9 import sparta_90ad52a9f3,sparta_a8839d110c
def sparta_d64693454d(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_8d581eb69e():
	if sparta_a8839d110c():A='/app/APPDATA/local_db/db.sqlite3'
	else:C=sparta_90ad52a9f3();B=os.path.join(C,'data');sparta_d64693454d(B);A=os.path.join(B,'db.sqlite3')
	return A