import os
from project.sparta_3d2a895074.sparta_97ad16475d.qube_745d53d6a8 import qube_745d53d6a8
from project.sparta_3d2a895074.sparta_97ad16475d.qube_0f569f923e import qube_0f569f923e
from project.sparta_3d2a895074.sparta_97ad16475d.qube_9f3c9bf8db import qube_9f3c9bf8db
from project.sparta_3d2a895074.sparta_97ad16475d.qube_ea68b3e575 import qube_ea68b3e575
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_745d53d6a8()
		elif A.dbType==1:A.dbCon=qube_0f569f923e()
		elif A.dbType==2:A.dbCon=qube_9f3c9bf8db()
		elif A.dbType==4:A.dbCon=qube_ea68b3e575()
		return A.dbCon