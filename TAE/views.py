import pandas as pd
import glob
import mimetypes
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import TAESheet, MasterTAE
from .forms import TAEUploadForm


from .forms import TAEUploadMultiForm

base_dir = settings.BASE_DIR
# Create your views here.
def TAEUpload(request):
    if request.method == "POST":
        form = TAEUploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = TAESheet(docfile = request.FILES['docfile'])
            newdoc.save()
            messages.success(request, "File upload Success")
    else:
        form = TAEUploadForm()
        
    return render(request, 'TAEupload.html', {'form' : form})


def upload_multiple(request):
    if request.method == "POST":
        form = TAEUploadMultiForm(request.POST, request.FILES)
        docfiles = request.FILES.getlist('docfile')
        print(docfiles)
        if form.is_valid():
            for f in docfiles:
                newdoc = TAESheet(docfile = f)
                newdoc.save()
            # context = {'msg' : '<span style="color: green;">File successfully uploaded</span>'}
            # return render(request, "MultiTAE.html", context)
#=====================================================================================================
            path = str(base_dir) + "/media/documents/TAE"
            file_list = glob.glob(path+"/*.xlsx")

            excl_list = []

            for file in file_list:
                excl_list.append(pd.read_excel(file))

            excl_merged = pd.DataFrame()

            for excl_file in excl_list:
                excl_merged = excl_merged.append(excl_file, ignore_index=True)
            
            excl_merged.to_excel(str(base_dir)+"/media/TAE_Merged.xlsx", index=False)
            masterTAE = open(str(base_dir)+"/media/TAE_Merged.xlsx", 'rb')
            empexceldata = pd.read_excel(masterTAE)
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                print(dbframe)
                obj = MasterTAE.objects.create(User_Name=dbframe._1,Location=dbframe.Location, Date=dbframe.Date,
                                                Project=dbframe.Project, Project_Task=dbframe._5, Activity=dbframe.Activity, 
                                                Role=dbframe.Role, Internal_Note=dbframe._8, Bill_Rate=dbframe._9,Bill_Hrs=dbframe._10,
                                                NB_Hrs=dbframe._11, Total_Hrs=dbframe._12, Revenue_Reason=dbframe._13)           
                obj.save()
            downloadfile = str(base_dir)+"/media/TAE_Merged.xlsx"

            #deleting residue files

            files = TAESheet.objects.all()
            for file in files:
                file.docfile.delete()
                file.delete()
#======================================================================================================
            return render(request, "download_merged.html", {'file' : downloadfile})
    else:
        form = TAEUploadMultiForm()
    return render(request, 'MultiTAE.html', {'form':form})


def deleteTAE(request):
    files = TAESheet.objects.all()
    for file in files:
        file.docfile.delete()
        file.delete()
    
    return HttpResponse("Files removed successfully")


def downloadTAE(request):
    filename = 'TAE_Merged.xlsx'
    file_path = settings.MEDIA_ROOT+'/'+filename

    fl = open(file_path,'rb')
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['X-Sendfile'] = file_path
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def summaryTAE(request):
    ls = {}
    objs = MasterTAE.objects.all()
    names = MasterTAE.objects.values_list('User_Name').distinct()
    for name in names:
        print(name[0])
        sum = 0
        for obj in objs.filter(User_Name = name[0]):
            sum += int(obj.Total_Hrs)
        ls[name[0]] = sum

    print(ls)

    return render(request, "summaryTAE.html", {'ls':ls})