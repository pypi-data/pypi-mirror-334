import time
from project.logger_config import logger
def sparta_c91461134a():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_c91461134a()
def sparta_2087f2d748(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_900da81943():sparta_2087f2d748(False)