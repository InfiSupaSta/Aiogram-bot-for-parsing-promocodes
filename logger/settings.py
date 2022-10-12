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
        'errors_logfile': {
            '()': CustomFileHandler,
            'filename': 'bot_errors.log',
            'level': 'ERROR',
            'formatter': 'standard'
        },
        'new_users_logfile': {
            '()': CustomFileHandler,
            'filename': 'new_users.log',
            'level': 'INFO',
            'formatter': 'standard'
        }
    },

    'loggers': {
        'bot_errors_logger': {
            'level': 'ERROR',
            'handlers': ['console', 'errors_logfile']
        },
        'new_user_logger': {
            'level': 'INFO',
            'handlers': ['console', 'new_users_logfile']
        }
    },
}
