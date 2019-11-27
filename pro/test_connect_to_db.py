import traceback
import time

from django.db import connections
from django.db.utils import OperationalError


try_count = 20
latency = 5  # sec


db_conn = connections['default']
for i in range(try_count):
    print('Test to connect to the database '+str(i))

    try:
        c = db_conn.cursor()
    except OperationalError:
        print(traceback.format_exc(0))
        print('Retrying after %s seconds' % latency)
        time.sleep(latency)
    else:
        print('Connecting to the database - successfully')
        break
