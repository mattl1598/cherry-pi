activate_this = '/var/www/cherry-pi-prod/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/cherry-pi-prod/")
sys.path.append("/var/www/cherry-pi-prod/venv/lib/python3.7/site-packages")

from webapp import app as application
application.secret_key = '1bdae5187b1f46039424a2380a7496e1'
