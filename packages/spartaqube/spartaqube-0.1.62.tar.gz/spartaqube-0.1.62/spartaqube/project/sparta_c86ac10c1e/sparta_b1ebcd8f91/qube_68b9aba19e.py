import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_17ba3a3ab7():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_c7a261d7ba(userId):A=sparta_17ba3a3ab7();B=os.path.join(A,userId);return B
def sparta_07e0014326(notebookProjectId,userId):A=sparta_c7a261d7ba(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_fbc0b29def(notebookProjectId,userId):A=sparta_c7a261d7ba(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_131d0de508(notebookProjectId,userId,ipynbFileName):A=sparta_c7a261d7ba(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_4d708db388(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_07e0014326(B,C);G=sparta_c7a261d7ba(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_c32d0a5d88(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_4d708db388(A,B);C=f"{A}.zip";D=sparta_c7a261d7ba(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}