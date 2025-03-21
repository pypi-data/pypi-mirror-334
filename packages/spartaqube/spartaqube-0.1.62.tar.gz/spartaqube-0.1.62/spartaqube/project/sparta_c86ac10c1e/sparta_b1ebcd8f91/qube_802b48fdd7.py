import os,base64
HANDLED_TYPES=['pdf','png','jpg','jpeg']
def sparta_ef36dcac7a(fileName):
	A=fileName.split('.')[-1].lower()
	if A in HANDLED_TYPES:return True
	return False
def sparta_4f088e887c(filePath,fileName):
	A=fileName;B=dict();C=A.split('.')[-1].lower()
	if C in['pdf','png','jpg','jpeg']:
		with open(os.path.join(filePath,A),'rb')as D:E=base64.b64encode(D.read()).decode();B['data']=E
	return B