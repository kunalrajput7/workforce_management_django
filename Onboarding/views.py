from django.shortcuts import render
from .forms import ResourceForm
from .models import Resource
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from Authentication.models import UserRole, ApplicationUser
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.conf import settings


base_dir = str(settings.BASE_DIR)
# Create your views here.
def onboard(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Created Successfully")
    else :
        form = ResourceForm()
    return render(request, 'onboard.html', {'form' : form})

password1 = '1234567890'

def bulk_upload(request):
    if request.method == "POST":
        ExcelData = request.FILES['ExcelData']

        if not ExcelData.name.endswith('xlsx'):
            messages.info(request, "Wrong Format")
            return render(request, 'bulk_upload.html')
        
        fs = FileSystemStorage()
        filename = fs.save(ExcelData.name, ExcelData)             
        empexceldata = pd.read_excel(base_dir+"/media/"+filename)        
        dbframe = empexceldata
        for dbframe in dbframe.itertuples():
            print(dbframe)
            obj = Resource.objects.create(EmpCode=dbframe.EmpCode,EmpName=dbframe.EmpName, Grade=dbframe.Grade,
                                            Role=dbframe.Role, Location=dbframe.Location, Billed=dbframe.Billed, Status=dbframe.Status)           
            obj.save()

        source_data = Resource.objects.all()
        for data in source_data:
            if User.objects.filter(username=data.EmpCode).exists():
                continue
            user = User(
                username=data.EmpCode,
                password = make_password(password1),    
            )
            user.save()
            appuser = ApplicationUser(user=user)
            role = UserRole.objects.get(name="User")
            print('Roles getting succesfull', role)
            appuser.save()
            appuser.roles.add(role)
            appuser.save()
    return render(request, 'bulk_upload.html')


def details(request):
    source_data = Resource.objects.all()
    for data in source_data:
        if User.objects.filter(username=data.EmpCode).exists():
            continue
        user = User(
            username=data.EmpCode,
            password = make_password(password1),    
        )
        user.save()
        appuser = ApplicationUser(user=user)
        role = UserRole.objects.get(name="User")
        print('Roles getting succesfull', role)
        appuser.save()
        appuser.roles.add(role)
        appuser.save()
    return render(request, "user_home.html")