import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_3d2a895074.sparta_a9ab8ca11f import qube_f133ff8567,qube_d45fa0e8f6,qube_a80499f8e7,qube_c9084c8ab8,qube_bab8b52daf,qube_4296962028,qube_c03932f643,qube_226b388987,qube_044ccb0f4d
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
def sparta_f0ebd6ba6a(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_f0ebd6ba6a(qube_f133ff8567.StatusWS)),url('ws/notebookWS',sparta_f0ebd6ba6a(qube_d45fa0e8f6.NotebookWS)),url('ws/wssConnectorWS',sparta_f0ebd6ba6a(qube_a80499f8e7.WssConnectorWS)),url('ws/pipInstallWS',sparta_f0ebd6ba6a(qube_c9084c8ab8.PipInstallWS)),url('ws/gitNotebookWS',sparta_f0ebd6ba6a(qube_bab8b52daf.GitNotebookWS)),url('ws/xtermGitWS',sparta_f0ebd6ba6a(qube_4296962028.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_f0ebd6ba6a(qube_c03932f643.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_f0ebd6ba6a(qube_226b388987.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_f0ebd6ba6a(qube_044ccb0f4d.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)