_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_84d3710fc4():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_a08b2a99bb(objectToCrypt):A=objectToCrypt;C=sparta_84d3710fc4();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_1aab5ff216(apiAuth):A=apiAuth;B=sparta_84d3710fc4();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_6d97110970(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_25cf304163(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_6d97110970(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_27899ed9e5(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_6d97110970(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_7c8920b080(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_616b09b9de(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_7c8920b080(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_16577c4839(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_7c8920b080(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_2c3068033c(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_7ff9ca5dff(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_2c3068033c(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_a891600a0f(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_2c3068033c(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_afc6eeb856():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_21c3bcc7b4(objectToCrypt):A=objectToCrypt;C=sparta_afc6eeb856();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_c035a2b2c9(objectToDecrypt):A=objectToDecrypt;B=sparta_afc6eeb856();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)