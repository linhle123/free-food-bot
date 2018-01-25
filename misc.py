# import datetime
# now = datetime.datetime.now()
# print(now)
# import getdata
# getdata.print_events_info()
import datetime

today = datetime.datetime.now()
start = datetime.date.today() + datetime.timedelta(days=today.weekday())
if today.date() <= start:
    print("here")
else:
    print("sdf")
# today = datetime.date.today()
