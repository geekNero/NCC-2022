from .models import SetTime
from datetime import datetime
def time_difference(start,end):
    duration=end-start
    seconds = abs(duration.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return int(hours),int(minutes),int(seconds%60)
def active():
    t=datetime.now().astimezone()
    object=SetTime.objects.get(pk=1)
    return (t>=object.start_time and t<=object.final_time)
def time_left():
    t=datetime.now().astimezone()
    object=SetTime.objects.get(pk=1)
    if(active()):
        h,m,s=time_difference(object.final_time,t)
        return m+(60*h)
    return 0
def current_time():
    t=datetime.now().astimezone()
    object=SetTime.objects.get(pk=1)    
    if(active()):
        h,m,s=time_difference(object.start_time,t)
        return {'hours':h, 'minutes':m, 'seconds':s}
    return 0
