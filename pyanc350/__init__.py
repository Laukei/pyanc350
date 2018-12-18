import logging

logger = logging.getLogger(__name__)

try:
	import pyanc350.v2
	logger.info('found anc350v2.dll')
except OSError:
	logger.warning('could not find anc350v2.dll')

try:
	import pyanc350.v3
	logger.info('found anc350v3.dll')
except OSError:
	logger.warning('could not find anc350v3.dll')

try:
	import pyanc350.v4
	logger.info('found anc350v4.dll')
except OSError:
	logger.warning('could not find anc350v4.dll')