_A='windows'
import os,platform,getpass
def sparta_a8839d110c():
	try:A=str(os.environ.get('IS_REMOTE_SPARTAQUBE_CONTAINER','False'))=='True'
	except:A=False
	return A
def sparta_6e22f4088b():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_90ad52a9f3():
	if sparta_a8839d110c():return'/spartaqube'
	A=sparta_6e22f4088b()
	if A==_A:B=f"C:\\Users\\{getpass.getuser()}\\SpartaQube"
	elif A=='linux':B=os.path.expanduser('~/SpartaQube')
	elif A=='mac':B=os.path.expanduser('~/Library/Application Support\\SpartaQube')
	return B