# https://github.com/logdna/python/blob/master/README.md
import logging
import os
from logging import LogRecord as NativeLogRecord
from time import sleep

from logdna import LogDNAHandler


class LogRecord(NativeLogRecord):
    def __init__(self, source, level, app, lineno, msg, args, exc_info, **kwargs):
        super().__init__(source, level, app, lineno, msg, args, exc_info, **kwargs)

class Ingestion:
    timeout = 3

    def __init__(self, api_key: str = None, **options):
        if api_key is None:
            api_key = os.environ['LOGDNA_INGESTION_KEY']
        options['log_error_response'] = True
        self.client = LogDNAHandler(api_key, options)
        self.flag: str = ''

    def connect(self):
        self.flag = 'pending'
        raise_error = not self.client.log_error_response
        expected_error_msg = 'Please provide a valid ingestion key. Discarding flush buffer'

        class OnInvalidKey(logging.Handler):
            def __init__(self, i: Ingestion):
                super().__init__()
                self.i = i

            def emit(self, record):
                if record.levelno == logging.DEBUG and record.msg == expected_error_msg:
                    self.i.flag = 'failed'
                elif self.i.flag == 'pending':
                    self.i.flag = 'success'

        handler = OnInvalidKey(self)
        self.client.internalLogger.addHandler(handler)
        self.client.emit(LogRecord(
            source=self.client.internalLogger.name,
            level=logging.DEBUG,
            app='davidkhala-devops',
            lineno=0,
            msg='connected',
            args=(),
            exc_info=None,
        ))
        ticktock = 0
        while self.flag == 'pending':
            sleep(1)
            ticktock += 1
            if ticktock > Ingestion.timeout:
                break
        self.client.internalLogger.removeHandler(handler)
        if self.flag == 'failed':
            if raise_error:
                raise Exception(expected_error_msg)
            else:
                return False
        return True

    def attach(self, logger: logging.Logger):
        logger.addHandler(self.client)
