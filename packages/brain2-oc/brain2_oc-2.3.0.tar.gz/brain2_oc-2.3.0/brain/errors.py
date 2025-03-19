# coding=utf8
""" Errors

Brain error codes
"""

__author__ = "Chris Nasr"
__copyright__ = "Ouroboros Coding Inc"
__version__ = "1.0.0"
__email__ = "chris@ouroboroscoding.com"
__created__ = "2023-01-16"

# Limit imports
__all__ = [
	'BAD_CONFIG', 'BAD_OAUTH', 'BAD_PORTAL', 'body', 'INTERNAL_KEY',
	'PASSWORD_STRENGTH', 'SIGNIN_FAILED'
]

# Import body errors
from body import errors as body

SIGNIN_FAILED = 1200
"""Sign In Failed"""

PASSWORD_STRENGTH = 1201
"""Password not strong enough"""

BAD_PORTAL = 1202
"""Portal doesn't exist, or the user doesn't have permissions for it"""

INTERNAL_KEY = 1203
"""Internal key failed to validate"""

BAD_OAUTH = 1204
"""Something failed in the OAuth process"""

BAD_CONFIG = 1205
"""Something is missing from the configuration"""