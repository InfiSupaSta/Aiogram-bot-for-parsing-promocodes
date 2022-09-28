from .handlers import CustomFileHandler

config_settings = {
    'version': 1,

    'formatters': {
        'standard': {
            'format': '\n{asctime} - {name} - {levelname} - {filename} - {funcName} - {message}',
            'style': '{'
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            '()': CustomFileHandler,
            'filename': 'bot_errors.log',
            'level': 'DEBUG',
            'formatter': 'standard'
        }
    },

    'loggers': {
        'bot_errors_logger': {
            'level': 'ERROR',
            'handlers': ['console', 'file']
        }
    },
}
