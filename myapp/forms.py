from django import forms
from django.forms import ModelForm
from myapp.models import myapp


#Form to CSV file Updation
class UploadFileForm(forms.Form):
    file = forms.FileField(help_text='CSV fields should be in exact same order that is "title | description | imageLocation | vedioLocation " ')
    header = forms.BooleanField(label="Does CSV contain Header ?", required = False)
    title = forms.BooleanField(label="Does it contain title ?", required = False)
    description = forms.BooleanField(label="Does it contain description ?", required = False)

#Form to access myapp Model(DB) 
class myappForm(ModelForm):
    class Meta:
        model = myapp
        fields = ["title","description","latitude","longitude"]

#Form to Form Image and Video Uploading
class imgVDFileForm(forms.Form):
    place_id = forms.IntegerField()
    file = forms.FileField(help_text="select a image of vedio : ", required = False)
    img = forms.BooleanField(label="Is this a Image?", required = False)
    vdo = forms.BooleanField(label="Is this a Vedio?", required = False)


#Custom Login Form 
class LoginForm(forms.Form):
   username = forms.CharField(widget=forms.TextInput)
   password = forms.CharField(widget=forms.PasswordInput)