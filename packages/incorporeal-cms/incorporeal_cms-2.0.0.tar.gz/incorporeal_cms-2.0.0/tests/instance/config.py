"""Configure the test application.

SPDX-FileCopyrightText: © 2020 Brian S. Stephan <bss@incorporeal.org>
SPDX-License-Identifier: GPL-3.0-only
"""

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s %(levelname)-7s %(name)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'incorporealcms.mdx': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'incorporealcms.pages': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
