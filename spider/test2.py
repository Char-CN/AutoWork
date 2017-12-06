


import datetime
import sys

if len(sys.argv) > 4 :
    begin_date = str(sys.argv[3])
    end_date = str(sys.argv[4])
elif len(sys.argv) > 3 :
    begin_date = str(sys.argv[3])
    end_date = str(sys.argv[3])
else :
    begin_date = str(datetime.date.today() - datetime.timedelta(days=1))
    end_date = begin_date

begin = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
  
d = begin  
delta = datetime.timedelta(days=1)
while d <= end:  
    print d.strftime("%Y-%m-%d")  
    d += delta
