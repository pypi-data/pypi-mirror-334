_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_92333e4c9d():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_edf6e30318(objectToCrypt):A=objectToCrypt;C=sparta_92333e4c9d();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_34acef52b0(apiAuth):A=apiAuth;B=sparta_92333e4c9d();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_588b7d5d1c(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_6acd99b46d(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_588b7d5d1c(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_4bbcbabc26(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_588b7d5d1c(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_2fe4f34431(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_6116ce8973(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_2fe4f34431(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_27bbbdde06(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_2fe4f34431(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_def51a0b43(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_c63c809b12(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_def51a0b43(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_cdb2e419e4(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_def51a0b43(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_9707dd6b98():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_f0f4ef6dc9(objectToCrypt):A=objectToCrypt;C=sparta_9707dd6b98();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_e67769de2a(objectToDecrypt):A=objectToDecrypt;B=sparta_9707dd6b98();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)