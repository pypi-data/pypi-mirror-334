import json,base64,websocket
from channels.generic.websocket import WebsocketConsumer
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.sparta_aac227c3fb.sparta_6ed1dc9d1a import qube_48e36c2566 as qube_48e36c2566
from project.logger_config import logger
class GitNotebookWS(WebsocketConsumer):
	channel_session=True;http_user_and_session=True
	def connect(A):A.accept();A.user=A.scope['user'];A.json_data_dict=dict()
	def disconnect(A,close_code):
		try:A.close()
		except:pass
	def sendStatusMsg(A,thisMsg):B={'res':3,'statusMsg':thisMsg};A.send(text_data=json.dumps(B))
	def receive(A,text_data):
		B=text_data;logger.debug('RECEIVE GIT INSTALL');logger.debug('text_data > ');logger.debug(B)
		if len(B)>0:C=json.loads(B);A.json_data_dict=C;D=qube_48e36c2566.sparta_aefad3f849(A,C,A.user);A.send(text_data=json.dumps(D));logger.debug('FINISH SOCKET')