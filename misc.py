# import datetime
# now = datetime.datetime.now()
# print(now)
# import getdata
# getdata.print_events_info()
# import datetime

# start = datetime.date.today() + datetime.timedelta(days=today.weekday())
# if today.date() <= start:
#     print("here")
# else:
#     print("sdf")
# today = datetime.date.today()

import os
import datetime
def last_modified_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

today = datetime.datetime.now()
print(today.date())
last_mod = last_modified_date("README.md").date()
if today.date() == last_mod:
    print("same date")
else:
    print("modified {} days ago on {}".format((today.date() - last_mod).days, last_mod))

# print(type(modification_date("events_today.pkl").date()))
