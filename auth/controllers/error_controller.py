
from bottle import HTTPError, error, response

import logging
logger = logging.getLogger(__name__)

@error(404)
@error(500)
def http_error(error):
    logger.error(error.traceback)
    response.content_type = 'application/json'
    return '{"error": "Please excuse my error. "}'
