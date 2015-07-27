__author__ = 'ockhius'

import logging
from django.conf import settings
from logging.handlers import SocketHandler, DEFAULT_TCP_LOGGING_PORT
import time

logger = logging.getLogger('RequestLog')
socketh = SocketHandler('localhost',DEFAULT_TCP_LOGGING_PORT)
logger.addHandler(socketh)
class RequestLoggingMiddleware:
    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        try:
            remote_addr = request.META.get('REMOTE_ADDR')
            if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
                remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
            user_email = "-"
#            extra_log = ""
            if hasattr(request,'user'):
                user_email = getattr(request.user, 'email', '-')
            req_time = time.time() - self.start_time
#            content_len = len(response.content)

            logger.info("%s#%s#%s#%s#%s#(%.02f seconds)" % (remote_addr, user_email, request.method, request.get_full_path(), response.status_code, req_time))
        except Exception, e:
            logger.error("LoggingMiddleware Error: %s" % e)
        return response

#    def process_request(self, request):
#        type = request.method
#        client_ip = request.META['REMOTE_ADDR']
#        date = datetime.fromtimestamp(int(time.mktime(datetime.now().timetuple())))
#        log = RequestLog(date=date, client_ip=client_ip, type=type)

#        log.save()

#        logger.debug(request)

#        return None

