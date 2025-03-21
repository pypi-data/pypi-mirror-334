import time
from project.logger_config import logger
def sparta_efc16b03c2():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_efc16b03c2()
def sparta_3c60e7abdc(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_947a10e216():sparta_3c60e7abdc(False)