import logging as py_logging
import sys

class LoggingWrapper(object):
    LOGGING_LEVELS = {
        'debug': py_logging.DEBUG,
        'info': py_logging.INFO,
        'warning': py_logging.WARNING,
        'error': py_logging.ERROR,
        'critical': py_logging.CRITICAL
    }
    
    def debug(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('debug', msg, caller, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('info', msg, caller, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('warning', msg, caller, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('error', msg, caller, *args, **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('critical', msg, caller, *args, **kwargs)
    
    def log(self, level, msg, source=None, *args, **kwargs):
        if not source:
            source = sys._getframe(1).f_globals['__name__']

        logger = self.get_logger(source)
        kwargs.update(source=source)
        logger.log(level=self.LOGGING_LEVELS[level], msg=msg, extra=kwargs)
    
    def get_logger(self, source):
        from django.conf import settings
        
        chunks = source.split('.')
        modules = ['.'.join(chunks[0:n]) for n in range(1, len(chunks) + 1)]
        modules.reverse()
        
        for source in modules:
            if source in settings.LOGGING:
                return py_logging.getLogger(source)
        
        return py_logging.getLogger('') # root logger

logging = LoggingWrapper()