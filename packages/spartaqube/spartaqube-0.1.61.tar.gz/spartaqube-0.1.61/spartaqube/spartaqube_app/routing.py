import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_1df4957b8d.sparta_594f7bd8d5 import qube_3533d3de25,qube_c8369f01e6,qube_e43bb78103,qube_5431abf54a,qube_f73c55a507,qube_c9f30167ea,qube_5f1a9c9935,qube_bff7cef3c4,qube_f48fe6e6a9
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
def sparta_a51c96cf83(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_a51c96cf83(qube_3533d3de25.StatusWS)),url('ws/notebookWS',sparta_a51c96cf83(qube_c8369f01e6.NotebookWS)),url('ws/wssConnectorWS',sparta_a51c96cf83(qube_e43bb78103.WssConnectorWS)),url('ws/pipInstallWS',sparta_a51c96cf83(qube_5431abf54a.PipInstallWS)),url('ws/gitNotebookWS',sparta_a51c96cf83(qube_f73c55a507.GitNotebookWS)),url('ws/xtermGitWS',sparta_a51c96cf83(qube_c9f30167ea.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_a51c96cf83(qube_5f1a9c9935.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_a51c96cf83(qube_bff7cef3c4.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_a51c96cf83(qube_f48fe6e6a9.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)