import os, sys

SECRET_KEY = os.environ.get("SECRET_KEY", None)
if SECRET_KEY == None:
    print("No SECRET_KEY key found")
    sys.exit(1)

ADMIN    = 1
CUSTOMER = 2
