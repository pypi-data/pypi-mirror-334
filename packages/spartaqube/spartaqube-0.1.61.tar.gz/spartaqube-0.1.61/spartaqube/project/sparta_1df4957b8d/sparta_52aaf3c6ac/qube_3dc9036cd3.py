import os
from project.sparta_1df4957b8d.sparta_52aaf3c6ac.qube_08ab94ffd8 import qube_08ab94ffd8
from project.sparta_1df4957b8d.sparta_52aaf3c6ac.qube_c420d9ab98 import qube_c420d9ab98
from project.sparta_1df4957b8d.sparta_52aaf3c6ac.qube_03d67dabee import qube_03d67dabee
from project.sparta_1df4957b8d.sparta_52aaf3c6ac.qube_8da79ca04c import qube_8da79ca04c
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_08ab94ffd8()
		elif A.dbType==1:A.dbCon=qube_c420d9ab98()
		elif A.dbType==2:A.dbCon=qube_03d67dabee()
		elif A.dbType==4:A.dbCon=qube_8da79ca04c()
		return A.dbCon