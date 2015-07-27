from logging.handlers import RotatingFileHandler
import datetime as dt

__author__ = 'ockhius'

import logging
import datetime
from evrekaTest.models import RequestErrorLog


class ReqDbLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            log = RequestErrorLog(level=record.levelname, message=record.message, date=datetime.datetime.now())
            log.save()
        except:
            pass

        return

class CustomTimeFormatter(logging.Formatter):
    converter=dt.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            #t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s%03d" % (int(record.created), record.msecs)
        return s


class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, *args, **kwargs):
        super(CustomRotatingFileHandler, self).__init__(filename,*args, **kwargs)
        formatter = CustomTimeFormatter(fmt="%(asctime)s#%(levelname)s#%(message)s#")
        self.setFormatter(formatter)

    def shouldRollover(self, record):
        """
        Check if CURRENT byte count exceeds maxBytes.
        """
        if self.stream is None:  # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:  # are we rolling over?
            # msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() >= self.maxBytes:
                return 1
        return 0