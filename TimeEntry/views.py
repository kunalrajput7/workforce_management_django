from django.shortcuts import render
from calendar import monthcalendar
from .models import Attendance
# import json

# Create your views here.
def calendar(request, year, month):
    cal = monthcalendar(year, month)
    user = request.user
    ls = []
    att = Attendance.objects.filter(EmpCode = user)
    for i in att:
        ls.append(i.Status)
    
    # lst = json.dumps(ls)

    
    if request.method == 'POST':
        
        res = request.POST
        print(res)
        for key, status in res.items():
            if(key != 'csrfmiddlewaretoken'):
                attendance = Attendance()
                date = f'{key}-{month}-{year}'
                print(date, status)
                if not Attendance.objects.filter(EmpCode = user, Date = date).exists():
                    attendance.EmpCode = str(user)
                    attendance.Date = date
                    attendance.Status = status
                    attendance.save()
                else:
                    rec = Attendance.objects.filter(EmpCode = user, Date = date).first()
                    rec.Status = status
                    rec.save()
        
    
    return render(request, "calendar.html" , {'cal':cal, 'year':year, 'month':month, 'lst':ls})

def summary(request):
    user = request.user
    att = Attendance.objects.filter(EmpCode = user)
    sum = 0
    for a in att:
        if a.Status == "Working":
            sum+=1
        if a.Status == "HalfDay":
            sum+=0.5
    
    cons = str(sum) + ' / ' + str(len(att))

    return render(request, 'summary.html', {'att': att, 'sum':cons})