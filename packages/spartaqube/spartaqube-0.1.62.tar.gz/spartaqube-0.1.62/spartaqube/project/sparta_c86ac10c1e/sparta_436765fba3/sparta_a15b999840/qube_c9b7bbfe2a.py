import time
from project.sparta_c86ac10c1e.sparta_436765fba3.qube_6e5996bfb0 import EngineBuilder
from project.logger_config import logger
class MysqlConnector(EngineBuilder):
	def __init__(A,host,port,user,password,database):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='mysql');A.connector=A.connect_db()
	def connect_db(A):return A.build_mysql()
	def test_connection(A):
		B=False
		try:
			if A.connector.is_connected():A.connector.close();return True
			else:return B
		except Exception as C:logger.debug(f"Error: {C}");return B