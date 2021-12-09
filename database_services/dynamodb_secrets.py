import os

# if you would prefer to write out your keys here when developing locally,
#   * set the following bool to be false
#   * fill out lines 14-16 with your keys
# REMEMBER: DO NOT COMMIT OR PUSH CHANGES TO THIS FILE!!!
USE_ENV_VARIABLES = True

if USE_ENV_VARIABLES:
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', None)
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY', None)
    AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', None)
else:
    AWS_ACCESS_KEY = ''
    AWS_SECRET_KEY = ''
    AWS_REGION_NAME = ''
