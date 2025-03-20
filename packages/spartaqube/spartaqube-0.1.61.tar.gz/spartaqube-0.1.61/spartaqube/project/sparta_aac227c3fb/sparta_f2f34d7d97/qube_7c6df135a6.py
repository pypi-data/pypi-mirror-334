import json,base64,asyncio,subprocess,uuid,os,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_aac227c3fb.sparta_27c3b9783a import qube_02cd768c6f as qube_02cd768c6f
from project.sparta_aac227c3fb.sparta_edc0f09f30 import qube_29eaa234f2
from project.sparta_aac227c3fb.sparta_88338b39fb import qube_87292c0503 as qube_87292c0503
from project.sparta_aac227c3fb.sparta_edc0f09f30.qube_03a4debf8e import Connector as Connector
from project.logger_config import logger
def sparta_9eff332b42(json_data,user_obj):
	D='key';A=json_data;logger.debug('Call autocompelte api');logger.debug(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_350399dbc7(B)
	return{'res':1,'output':C,D:B}
def sparta_350399dbc7(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";H={'http':os.environ.get('http_proxy',None),'https':os.environ.get('https_proxy',None)};C=requests.get(G,proxies=H)
	try:
		if int(C.status_code)==200:
			I=json.loads(C.text);D=I['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]