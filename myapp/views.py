from django.shortcuts import render , render_to_response, redirect
from django.http import HttpResponse
from .models import myapp , imageLoc , VideoLoc
from django.views.decorators.csrf import csrf_exempt
from .forms import UploadFileForm , myappForm ,imgVDFileForm , LoginForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import pandas as pd
from django.forms import formset_factory
import json




# Create your views here.
#it will be called when adminpanel is requested
def index(request,message=""):
    #checking if the user is authenticated if yes rendering the page 
    if request.user.is_authenticated:
        message = "Welcome "+str(request.user.username)+" to Admin panel ..." if message == "" else message
        return render(request,'index.html', { "message" : message })            #rendering Adminpanel page
    
    #if user is not authenticated and its a POST request then it will take Login Form data and check for authentication  
    elif request.method =="POST":
        form = LoginForm(request.POST)     #loading Login form from the .forms in the top
        #checking the form passed is valid or not
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user = authenticate(request,username=username,password=password)           #getting user from given username and password if not found then it will return None
            #checking the authentication value if user existed it will give true 
            if user!=None and user.is_authenticated:
                login(request,user)        #login in the user to the django authenticaton system
                #rendering the admin panel
                message = "Welcome "+str(request.user.username)+" to Admin panel" if message == "" else message
                return render(request,'index.html', {"base":"adminpanel","message" : message})           #rendering Adminpanel page
    

        #if form is invalid it will ask for the login again
        form = LoginForm()                 #loading Login form from the .forms in the top
        message = "Please Enter a Valid Username & Password"
        return render(request,'registration/login.html',{"form":form,"message" : message})           #rendering Login page

    #if it is the GET request asking for login details
    else:
        form = LoginForm()                 #loading Login form from the .forms in the top
        message = "Please Login for Moving Further"
        return render(request,'registration/login.html',{"form":form,"message" : message})           #rendering Login page




# this is called when we have to "change" the image/Video status or To "delete" image or record     --- and is called by Result_script.js using AJAX 
def status(request):
    #Storing the new State from the signal state
    new_status = "Approved" if request.POST["status"] == "UnApproved" else "UnApproved" if request.POST["status"] == "Approved" else request.POST["status"]
    #this if will execute if the signal was of "Approved" or "unapproved"
    if new_status == "UnApproved" or new_status == "Approved":
        #checking the file type of the signal image
        if request.POST["file_type"] == "image":
            imgData = imageLoc.objects.get(id = int(request.POST["id"]))    #Fetching the data from the imageLoc table using "id" of the signal
            imgData.status = new_status    #updating the state
            imgData.save()
        #checking the file type of the signal video        
        else:
            vdoData = VideoLoc.objects.get(id = int(request.POST["id"]))   #Fetching the data from the VideoLoc table using "id" of the signal
            vdoData.status = new_status    #updating the state
            vdoData.save()

    #If the signal was of delete then
    elif request.POST["status"] == "Delete":
        #checking the file type of the signal --image
        if request.POST["file_type"] == "image":
            imgData = imageLoc.objects.get(id = int(request.POST["id"]))   #Fetching the data from the imageLoc table using "id" of the signal
            imgData.delete()                                               #deleting the data

        #checking the file type of the signal --vedio        
        elif request.POST["file_type"] == "video":
            vdoData = VideoLoc.objects.get(id = int(request.POST["id"]))   #Fetching the data from the VideoLoc table using "id" of the signal
            vdoData.delete()                                               #deleting the data

        #checking the file type of the signal --record        
        elif request.POST["file_type"] == "record":
            myappData = myapp.objects.get(id = int(request.POST["id"]))    #Fetching the data from the myapp table using "id" of the signal
            myappData.delete()                                             #deleting the data

            imgData = imageLoc.objects.filter(place_id = int(request.POST["id"]))   #Fetching the data from the imageLoc table using "id" of the signal
            for img_instance in imgData:                                            #deleting the all image dta
                img_instance.delete()
            vdoData = VideoLoc.objects.filter(place_id = int(request.POST["id"]))   #Fetching the data from the VideoLoc table using "id" of the signal
            for vdo_instance in vdoData:
                vdo_instance.delete()                                               #deleting the all video dta

    id = request.POST["id"]
    return JsonResponse({"file_type":request.POST["file_type"]})                    #sending the response to AJAX




#this will be called by admin_script.js using AJAX --- to get the result of the searched text in the adminpanel
def admin_search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
    #storing top "6" records containing that search text 
    articles = myapp.objects.filter(title__icontains=str(search_text))[:6]
    return render_to_response('admin_search.html',{'articles':articles})      # rendering results into admin panel 





#this is Called by the Unapprovied Tab from the navigation from the admin side
def UnApprovedlist(request):
    #checking for user authentication "only user can access these features"
    if request.user.is_authenticated:
        imgData = imageLoc.objects.filter(status = "UnApproved")         #collecting all unapproved images
        vdoData = VideoLoc.objects.filter(status = "UnApproved")         ##collecting all unapproved videos

        place_ids = list(set(int(entry.place_id) for entry in imgData))         #making a set of ids of these unapproved images
        place_ids_1 = list(set(int(entry.place_id) for entry in vdoData))       #making a set of ids of these unapproved video
        total_place_ids = list(set(place_ids + place_ids_1))                    #making set of all these images and video ids
        
        results = []
        for idx in total_place_ids:
            try:
                results.append(myapp.objects.get(id=idx))                        # storing data of all the unapproved ids
            except:
                continue

        message = "List of all the UnApproved Records."
        return render(request,"SelcetedList.html",{"results":results,"message":message})       #rendering the results in selectedlist.html with a message

    #if user is not authenticated ask for login 
    else:
        form = LoginForm()                         #login form 
        message = "Please Login for Moving Further"
        return render(request,'registration/login.html',{"form":form,"message" : message})     # rendering login page





#this is Called by the Approvied Tab from the navigation from the admin side
def Approvedlist(request):
    #checking for user authentication "only user can access these features"
    if request.user.is_authenticated:
        imgData = imageLoc.objects.filter(status = "Approved")           #collecting all approved images
        vdoData = VideoLoc.objects.filter(status = "Approved")           #collecting all approved videos

        place_ids = list(set(int(entry.place_id) for entry in imgData))         #making a set of ids of these approved images
        place_ids_1 = list(set(int(entry.place_id) for entry in vdoData))       #making a set of ids of these approved video
        total_place_ids = list(set(place_ids + place_ids_1))                    #making set of all these images and video ids
        
        results = []
        for idx in total_place_ids:
            try:
                results.append(myapp.objects.get(id=idx))                        # storing data of all the approved ids
            except:
                continue

        message = "List of all the Approved Records."
        return render(request,"SelcetedList.html",{"results":results,"message":message})         #rendering the results in selectedlist.html with a message

    #if user is not authenticated ask for login 
    else:
        form = LoginForm()                        #login form 
        message = "Please Login for Moving Further"
        return render(request,'registration/login.html',{"form":form,"message" : message})       # rendering login page



#this is Called by the All Data Tab from the navigation from the admin side
def AllDatalist(request):
    #checking for user authentication "only user can access these features"
    if request.user.is_authenticated:
        results = myapp.objects.filter()                                   # storing all the data 
        message = "List of all the Records."
        return render(request,"SelcetedList.html",{"results":results,"message":message})              #rendering the results in selectedlist.html with a message

    #if user is not authenticated ask for login 
    else:
        form = LoginForm()              #login form
        message = "Please Login for Moving Further"
        return render(request,'registration/login.html',{"form":form,"message" : message})      # rendering login page






#this is Called by the csv upload Tab from the navigation from the admin side
def csvUpload(request,message=""):
    #checking for user authentication "only user can access these features"
    if request.user.is_authenticated:
        form = UploadFileForm()     #loading UploadCSV form from froms.py file -----imported above
        message = "Upload s csv using below form" if message == "" else message
        return render(request,'csvUpload.html',{"form":form,"message":message})           #rendering the csv form in csvUpload.html with a message

    #if user is not authenticated ask for login 
    else:
        form = LoginForm()            #login form
        message = "Please Login for Moving Further" if message == "" else message
        return render(request,'registration/login.html',{"form":form,"message" : message})          # rendering login page



#this is Called by the Result html pages asking for updation/adding in the place data , images and vedios  -----only for admin
def Insert_data(request):
    #checking for user authentication "only user can access these features"
    if request.user.is_authenticated:
        #checking if it is a post method then proced
        if request.method == 'POST':
            data_form = myappForm(request.POST)           #loading the myappform from the Request parameters
            if data_form.is_valid():                      #checking for validation
                if request.POST["place_id"] != "None" :               #if place id not none then update the existing data 
                    db_ptr = myapp(
                                id = int(request.POST["place_id"]),
                                title = data_form.cleaned_data["title"],
                                description = data_form.cleaned_data["description"],
                                longitude=data_form.cleaned_data["longitude"],
                                latitude=data_form.cleaned_data["latitude"],
                                placevalue=data_form.cleaned_data["placevalue"],
                                placetitle=data_form.cleaned_data["placetitle"]
                            )
                else:                                                  #if place id none then add the new data 
                    db_ptr = myapp(
                                title = data_form.cleaned_data["title"],
                                description = data_form.cleaned_data["description"],
                                longitude=data_form.cleaned_data["longitude"],
                                latitude=data_form.cleaned_data["latitude"],
                                placevalue=data_form.cleaned_data["placevalue"],
                                placetitle=data_form.cleaned_data["placetitle"]
                            )
                db_ptr.save()

            place_id = db_ptr.id                                    # storing id of the myapp data
            if not request.POST._mutable:                           #making request mutable  so that we can validate forms by adding nessary fields
                request.POST._mutable = True

            request.POST["place_id"]=place_id                       #adding place_id for new datas 
            form = imgVDFileForm(request.POST, request.FILES )      #loading the imgVDFileForm from the Request parameters

            if form.is_valid():                                     #validaing and add the data if valid the values
                if form.cleaned_data['img']:
                    newimg = imageLoc(place_id=place_id ,imageLocation=request.FILES['file'] , status = "Approved")
                    newimg.save()

                if form.cleaned_data['vdo']:
                    newimg = VideoLoc(place_id=place_id ,vedioLocation=request.FILES['file'] , status = "Approved")
                    newimg.save()
                
                return redirect("admin_result", num=place_id)      #redirect to admin _results with the newly generated id

        return admin_result(request,num=place_id,message="Failed!!! Record has Not been Added...")              # redirecting with error message 
    #if user is not authenticated ask for login 
    else:
        form = LoginForm()
        message = "Please Login for Moving Further"
        return render(request,'registration/login.html',{"form":form,"message" : message})


#this is Called when a Place card is clicked for more, shows data and images of the particular place  -----only for admin
def admin_result(request,num=0,message=""):
    #checking for user authentication "only user can access these features"
    if request.user.is_authenticated:
        if num!=0:                  #checking for new entry (0 == new entry)
            data = myapp.objects.get(id=num)                  #getting place details from mpapp  to use in default value 
            data_form = myappForm()                           #loading myapp form it will be used for updation time

            imgData = imageLoc.objects.filter(place_id=int(num))          #loading images and videos of that places using place id
            vdoData = VideoLoc.objects.filter(place_id=int(num))
            
            form = imgVDFileForm()                                        #loading imgVDFileForm form for taking in new image or vedio input
            message = "Update Place Data Using the Form above . . ." if message == "" else message

            values = { "title" : data.title , "description" : data.description , "place_id" : num ,"message" : message ,"latitude":data.latitude,'longitude':data.longitude,'placetitle':data.placetitle,'placevalue':data.placevalue}
            res = { "data_form" : data_form, "form" : form , "imgData" : imgData, "value":values , "vdoData" : vdoData}
            return render(request,'admin_result.html',{'res':res})        #rendering admin_result.html 

        else:                                       #if it is a new entry 
            data_form = myappForm()                 # loading all the forms for place data
            form  = imgVDFileForm()                 # for image and vedio inputs

            message = "Add Place Using the Form above . . ." if message == "" else message
            res = { "data_form" : data_form,"form" : form , "imgData" : {},"message":message}
            return render(request,'add_place.html',{'res':res})          #rendering add_place.html 

    #if user is not authenticated ask for login 
    else:
        form = LoginForm()
        message = "Please Login for Moving Further"
        return render(request,'registration/login.html',{"form":form,"message" : message})





#this is called by upload function only
def dbupdater(fptr,hdr,tle,Dscptn):
    #checking all the fields
    if hdr:
        dataframe = pd.read_csv(fptr)
    else:
        dataframe = pd.read_csv(fptr,header = None)
        
    #uploading one by one data from the dataframe of csv to DB
    for row in dataframe.values:
        title = row[0] if tle else "Not Available"
        description = row[1] if Dscptn else "Not Available"
        db_ptr = myapp(
                        title = title,
                        description = description
                    )
        db_ptr.save()


#this is called by csvUpload when form is submitted 
def upload(request):
    #checking for user authentication "only user can access these features"
    if request.user.is_authenticated:
        if request.method == 'POST':
            #print(request.POST)
            form = UploadFileForm(request.POST, request.FILES )                #loading form with request parameters
            if form.is_valid():                                                #if valid call dbupdater
                dbupdater(request.FILES['file'],form.cleaned_data['header'],form.cleaned_data['title'],form.cleaned_data['description'])
                return csvUpload(request,"SuccessFully Uploaded")

        return csvUpload(request,"Uploading Failed")

    #if user is not authenticated ask for login     
    else:
        form = LoginForm()
        message = "Please Login for Moving Further"
        return render(request,'registration/login.html',{"form":form,"message" : message})





#this will be called by ajax_script.js using AJAX --- to get the result of the searched text in the home
def search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
        results = myapp.objects.values_list('id').get(title=search_text)
        try:
            res=imageLoc.objects.values_list('imageLocation').get(place_id=results[0])
            res=res[0]
        except imageLoc.DoesNotExist:
            res=""
        try:
            types=VideoLoc.objects.values_list('vedioLocation').get(place_id=results[0])
            types=types[0]
        except VideoLoc.DoesNotExist:
            types=""
       
        response=myapp.objects.values_list('longitude','latitude').get(title=search_text)
    else:
        search_text = ''
    #storing top "6" records containing that search text     
    articles = myapp.objects.filter(title__icontains=str(search_text))[:6]
    return render_to_response('ajax_search.html',{'articles':articles,'images':res,'video':types,'lat':response[1],'long':response[0]})         #rendering these results in the Home

#this is Called when a Place card is clicked for more, shows data and images of the particular place ---and user can only add images/videos
def result(request,num=0,message="Upload Images & Vedios Using the Form above . . ."):
    data = myapp.objects.get(id=num)                                             # loading all the data of place id
    imgData = imageLoc.objects.filter(place_id=int(num),status = "Approved")     # loading all the images and videos with approve status
    vdoData = VideoLoc.objects.filter(place_id=int(num),status = "Approved")

    form = imgVDFileForm()
    res = { "data" : data , "form" : form , "imgData" : imgData , "vdoData" : vdoData, "message" : message }
    return render(request,'search_result.html',{'res':res})                    # rendering results into  search_results





#adding images from user side
def add_image_data(request):
    if request.method == 'POST':
        form = imgVDFileForm(request.POST, request.FILES )            #loading form for request
        if form.is_valid():                # saving file depending upon there signal if img is true it will be loaded in to images and vice versa
            if form.cleaned_data['img']:                              
                newimg = imageLoc(place_id=form.cleaned_data["place_id"] ,imageLocation=request.FILES['file'] , status = "UnApproved")
                newimg.save()

            if form.cleaned_data['vdo']:
                newimg = VideoLoc(place_id=form.cleaned_data["place_id"] ,vedioLocation=request.FILES['file'] , status = "UnApproved")
                newimg.save()

            return  result(request,num=form.cleaned_data["place_id"],message = "SuccessFully Uploaded!! Image is send to Admin For Approval...")
    return  result(request,num=form.cleaned_data["place_id"],message = "Failed!!! Please Try again with Valid File Type...")



#For rendering user Home page
def home(request):
    return render(request,'home.html', {"base":"home"})

#search place according to textbox value search
def serch_places(request):
     if request.method == 'GET':
        title = request.GET['title']
        results = myapp.objects.values_list('longitude','latitude','id').get(title=title)
        images=imageLoc.objects.values_list('imageLocation').get(place_id=results[2])
        response={
            'lat'   : results[0],
            'long'  : results[1],
            'images': images[0]
        }
        return HttpResponse(json.dumps(response)) 