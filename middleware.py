class LoggingMiddleware(object):
    def __init__(self):
        from django.conf import settings
        from django.core.exceptions import ImproperlyConfigured
        import logging
        
        for module, properties in settings.LOGGING.items():
            logger = logging.getLogger(module)
            
            if 'level' in properties:
                logger.setLevel(properties['level'])
            elif hasattr(settings, 'GLOBAL_LOG_LEVEL'):
                logger.setLevel(settings.GLOBAL_LOG_LEVEL)
            else:
                raise ImproperlyConfigured(
                    "A logger in settings.LOGGING doesn't have its log level set. " +
                    "Either set a level on that logger, or set GLOBAL_LOG_LEVEL.")
            
            if 'handler' in properties:
                handlers = [properties['handler']]
            elif 'handlers' in properties:
                handlers = properties['handlers']
            elif hasattr(settings, 'GLOBAL_LOG_HANDLERS'):
                handlers = settings.GLOBAL_LOG_HANDLERS

            for handler in handlers:
                if type(handler) is dict:
                    if 'format' in handler:
                        handler['handler'].setFormatter(logging.Formatter(handler['format']))
                    if 'level' in handler:
                        handler['handler'].setLevel(handler['level'])
                    logger.addHandler(handler['handler'])
                else:
                    logger.addHandler(handler)


    def process_exception(self, request, exception):
        from jogging import logging
        logging.critical("DOOOOOOOOOOM!!!!") # TODO