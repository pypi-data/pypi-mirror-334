_C='postgres'
_B='json_api'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_aac227c3fb.sparta_edc0f09f30.qube_29eaa234f2 as qube_29eaa234f2
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_b02ac4331a.qube_fd76637034 import AerospikeConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_d56460d732.qube_7dc4d58dae import CassandraConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_e4c21129f6.qube_67940b49fa import ClickhouseConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_441ee83290.qube_b48cb8de33 import CouchdbConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_8f0bb38ba9.qube_e2691712cd import CsvConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_93616e7fa3.qube_88f5e243e1 import DuckDBConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_97d5c7c43f.qube_3d38bad456 import JsonApiConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_99de2dc96b.qube_da747bf3f9 import InfluxdbConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_94dcae8f10.qube_36c78147c2 import MariadbConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_26c6e7486c.qube_11f45f8eb1 import MongoConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_fda31772ee.qube_3933236ca3 import MssqlConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_71a9ba2cd4.qube_a1015879a1 import MysqlConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_8032929bfd.qube_ba3520c6f8 import OracleConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_364ec56ffe.qube_05a8e12284 import ParquetConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_90eb1d9e44.qube_fb68a02723 import PostgresConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_b19c4bd4cf.qube_3e25df7e7e import PythonConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_ee975d3bc9.qube_c6dacb2536 import QuestDBConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_e5b8eb5de0.qube_b0ffd3e3b8 import RedisConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_58e04abbab.qube_342d2a0ac1 import ScylladbConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_36385eac8d.qube_d1950c937e import SqliteConnector
from project.sparta_aac227c3fb.sparta_edc0f09f30.sparta_56dbe71763.qube_8302c0e3e2 import WssConnector
from project.logger_config import logger
class Connector:
	def __init__(A,db_engine=_C):A.db_engine=db_engine
	def close_db(A):
		try:A.connector.close()
		except:pass
	def init_with_model(C,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:B=qube_29eaa234f2.sparta_f82d015da8(H)
		except:B=_A
		try:
			if A.password is not _A:B=A.password
		except:pass
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;C.db_engine=Q;C.init_with_params(host=E,port=F,user=G,password=B,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='cassandra':A.db_connector=CassandraConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='clickhouse':A.db_connector=ClickhouseConnector(host=B,port=C,database=F,user=D,password=E)
		if A.db_engine=='couchdb':A.db_connector=CouchdbConnector(host=B,port=C,user=D,password=E)
		if A.db_engine=='csv':A.db_connector=CsvConnector(csv_path=csv_path,csv_delimiter=csv_delimiter)
		if A.db_engine=='duckdb':A.db_connector=DuckDBConnector(database_path=G,read_only=read_only)
		if A.db_engine=='influxdb':A.db_connector=InfluxdbConnector(host=B,port=C,token=token,organization=organization,bucket=F,user=D,password=E)
		if A.db_engine==_B:A.db_connector=JsonApiConnector(json_url=json_url,dynamic_inputs=H,py_code_processing=I)
		if A.db_engine=='mariadb':A.db_connector=MariadbConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mongo':A.db_connector=MongoConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mssql':A.db_connector=MssqlConnector(host=B,port=C,trusted_connection=trusted_connection,driver=driver,user=D,password=E,database=F)
		if A.db_engine=='mysql':A.db_connector=MysqlConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='oracle':A.db_connector=OracleConnector(host=B,port=C,user=D,password=E,database=F,lib_dir=lib_dir,oracle_service_name=oracle_service_name)
		if A.db_engine=='parquet':A.db_connector=ParquetConnector(database_path=G)
		if A.db_engine==_C:A.db_connector=PostgresConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='python':A.db_connector=PythonConnector(py_code_processing=I,dynamic_inputs=H)
		if A.db_engine=='questdb':A.db_connector=QuestDBConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='redis':A.db_connector=RedisConnector(host=B,port=C,user=D,password=E,db=redis_db)
		if A.db_engine=='scylladb':A.db_connector=ScylladbConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='sqlite':A.db_connector=SqliteConnector(database_path=G)
		if A.db_engine=='wss':A.db_connector=WssConnector(socket_url=socket_url,dynamic_inputs=H,py_code_processing=I)
	def get_db_connector(A):return A.db_connector
	def test_connection(A):return A.db_connector.test_connection()
	def preview_output_connector_bowler(A):return A.db_connector.preview_output_connector_bowler()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_available_views(A):B=A.db_connector.get_available_views();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_B:return A.db_connector.get_json_api_dataframe()
		else:
			B=A.db_connector.get_data_table(table_name)
			if isinstance(B,pd.DataFrame):return B
			return pd.DataFrame(B)
	def get_data_table_top(A,table_name,top_limit=100):
		if A.db_engine==_B:return A.db_connector.get_json_api_dataframe()
		else:
			B=A.db_connector.get_data_table_top(table_name,top_limit)
			if isinstance(B,pd.DataFrame):return B
			return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)