_M='An error occurred, please try again'
_L='password_confirmation'
_K='password'
_J='jsonData'
_I='api_token_id'
_H='Invalid captcha'
_G='is_created'
_F='utf-8'
_E=None
_D='errorMsg'
_C=False
_B=True
_A='res'
import hashlib,re,uuid,json,requests,socket,base64,traceback,os
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings as conf_settings
from django.urls import reverse
from project.models import UserProfile,GuestCode,GuestCodeGlobal,LocalApp,SpartaQubeCode
from project.sparta_1df4957b8d.sparta_f6456b32f2.qube_4ed691eaf9 import sparta_6f00ce0a1c
from project.sparta_aac227c3fb.sparta_ddf73c7bad import qube_770d517101 as qube_770d517101
from project.sparta_aac227c3fb.sparta_b3647f8030 import qube_b5aadfcc12 as qube_b5aadfcc12
from project.sparta_aac227c3fb.sparta_77bdbeee4d.qube_127d156849 import Email as Email
from project.logger_config import logger
def sparta_993310294e(function):
	def A(request,*E,**D):
		A=request;B=_B
		if not A.user.is_active:B=_C;logout(A)
		if not A.user.is_authenticated:B=_C;logout(A)
		try:C=D.get(_I,_E)
		except:C=_E
		if not B:
			if C is not _E:F=qube_b5aadfcc12.sparta_4df0fb1c53(C);login(A,F)
		else:0
		return function(A,*E,**D)
	return A
def sparta_a362f1190b(function):
	def A(request,*C,**D):
		B='notLoggerAPI';A=request
		if not A.user.is_active:return HttpResponseRedirect(reverse(B))
		if A.user.is_authenticated:return function(A,*C,**D)
		else:return HttpResponseRedirect(reverse(B))
	return A
def sparta_afc9e300b0(function):
	def A(request,*B,**C):
		try:return function(request,*B,**C)
		except Exception as A:
			if conf_settings.DEBUG:logger.debug('Try catch exception with error:');logger.debug(A);logger.debug('traceback:');logger.debug(traceback.format_exc())
			D={_A:-1,_D:str(A)};E=json.dumps(D);return HttpResponse(E)
	return A
def sparta_771641a93a(function):
	C=function
	def A(request,*D,**E):
		A=request;F=_C
		try:
			G=json.loads(A.body);H=json.loads(G[_J]);I=H[_I];B=qube_b5aadfcc12.sparta_4df0fb1c53(I)
			if B is not _E:F=_B;A.user=B
		except Exception as J:logger.debug('exception pip auth');logger.debug(J)
		if F:return C(A,*D,**E)
		else:K='public@spartaqube.com';B=User.objects.filter(email=K).all()[0];A.user=B;return C(A,*D,**E)
	return A
def sparta_921332448f(code):
	try:
		B=SpartaQubeCode.objects.all()
		if B.count()==0:return code=='admin'
		else:C=B[0].spartaqube_code;A=hashlib.md5(code.encode(_F)).hexdigest();A=base64.b64encode(A.encode(_F));A=A.decode(_F);return A==C
	except Exception as D:pass
	return _C
def sparta_b4126b94ef():
	A=LocalApp.objects.all()
	if A.count()==0:B=str(uuid.uuid4());LocalApp.objects.create(app_id=B,date_created=datetime.now());return B
	else:return A[0].app_id
def sparta_12f5e39817():A=socket.gethostname();B=socket.gethostbyname(A);return B
def sparta_679d34cd9e(json_data):
	D='ip_addr';A=json_data;del A[_K];del A[_L]
	try:A[D]=sparta_12f5e39817()
	except:A[D]=-1
	C=dict();C[_J]=json.dumps(A);E={'http':os.environ.get('http_proxy',_E),'https':os.environ.get('https_proxy',_E)};B=requests.post(f"{conf_settings.SPARTAQUBE_WEBSITE}/create-user",data=json.dumps(C),proxies=E)
	if B.status_code==200:
		try:
			A=json.loads(B.text)
			if A[_A]==1:return{_A:1,_G:_B}
			else:A[_G]=_C;return A
		except Exception as F:return{_A:-1,_G:_C,_D:str(F)}
	return{_A:1,_G:_C,_D:f"status code: {B.status_code}. Please check your internet connection"}
def sparta_06aa966634(json_data,hostname_url):
	Q='emailExist';P='passwordConfirm';L='email';B=json_data;F={P:'The two passwords must be the same...',L:'Email address is not valid...','form':'The form you sent is not valid...',Q:'This email is already registered...'};E=_C;R=B['firstName'].capitalize();S=B['lastName'].capitalize();C=B[L].lower();M=B[_K];T=B[_L];U=B['code'];G=B['captcha'];B['app_id']=sparta_b4126b94ef()
	if G=='cypress'and C=='cypress_tests@gmail.com':0
	else:
		print('DEBUG CAPTACH');print(G);N=sparta_6f00ce0a1c(G);print('captcha_validator_dict');print(N)
		if N[_A]!=1:return{_A:-1,_D:_H}
	if not sparta_921332448f(U):return{_A:-1,_D:'Invalid spartaqube code, please contact your administrator'}
	if M!=T:E=_B;H=F[P]
	if not re.match('[^@]+@[^@]+\\.[^@]+',C):E=_B;H=F[L]
	if User.objects.filter(username=C).exists():E=_B;H=F[Q]
	if not E:
		V=sparta_679d34cd9e(B);O=_B;W=V[_G]
		if not W:O=_C
		A=User.objects.create_user(C,C,M);A.is_staff=_C;A.username=C;A.first_name=R;A.last_name=S;A.is_active=_B;A.save();D=UserProfile(user=A);I=str(A.id)+'_'+str(A.email);I=I.encode(_F);J=hashlib.md5(I).hexdigest()+str(datetime.now());J=J.encode(_F);X=str(uuid.uuid4());D.user_profile_id=hashlib.sha256(J).hexdigest();D.email=C;D.api_key=str(uuid.uuid4());D.registration_token=X;D.b_created_website=O;D.save();K={_A:1,'userObj':A};return K
	K={_A:-1,_D:H};return K
def sparta_d7c3b7db10(user_obj,hostname_url,registration_token):C='Validate your account';B=user_obj;A=Email(B.username,[B.email],f"Welcome to {conf_settings.PROJECT_NAME}",C);A.addOneRow(C);A.addSpaceSeparator();A.addOneRow('Click on the link below to validate your account');D=f"{hostname_url.rstrip('/')}/registration-validation/{registration_token}";A.addOneCenteredButton('Validate',D);A.send()
def sparta_cd3e44709f(token):
	C=UserProfile.objects.filter(registration_token=token)
	if C.count()>0:A=C[0];A.registration_token='';A.is_account_validated=_B;A.save();B=A.user;B.is_active=_B;B.save();return{_A:1,'user':B}
	return{_A:-1,_D:'Invalid registration token'}
def sparta_756547b696():return conf_settings.IS_GUEST_CODE_REQUIRED
def sparta_526b4cf4c2(guest_code):
	if GuestCodeGlobal.objects.filter(guest_id=guest_code,is_active=_B).count()>0:return _B
	return _C
def sparta_dcae1c7535(guest_code,user_obj):
	D=user_obj;C=guest_code
	if GuestCodeGlobal.objects.filter(guest_id=C,is_active=_B).count()>0:return _B
	A=GuestCode.objects.filter(user=D)
	if A.count()>0:return _B
	else:
		A=GuestCode.objects.filter(guest_id=C,is_used=_C)
		if A.count()>0:B=A[0];B.user=D;B.is_used=_B;B.save();return _B
	return _C
def sparta_e31221964a(user):
	A=UserProfile.objects.filter(user=user)
	if A.count()==1:return A[0].is_banned
	else:return _C
def sparta_1649502119(email,captcha):
	D=sparta_6f00ce0a1c(captcha)
	if D[_A]!=1:return{_A:-1,_D:_H}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_M}
	A=B[0];C=str(uuid.uuid4());A.token_reset_password=C;A.save();sparta_9bee8f1fe1(A.user,C);return{_A:1}
def sparta_9bee8f1fe1(user_obj,token_reset_password):B=user_obj;A=Email(B.username,[B.email],'Reset Password','Reset Password Message');A.addOneRow('Reset code','Copy the following code to reset your password');A.addSpaceSeparator();A.addOneRow(token_reset_password);A.send()
def sparta_351c945738(captcha,token,email,password):
	D=sparta_6f00ce0a1c(captcha)
	if D[_A]!=1:return{_A:-1,_D:_H}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_M}
	A=B[0]
	if not token==A.token_reset_password:return{_A:-1,_D:'Invalid token..., please try again'}
	A.token_reset_password='';A.save();C=A.user;C.set_password(password);C.save();return{_A:1}