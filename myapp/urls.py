from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('adminpanel', views.index, name='index'),
    path('adminpanel/(?P<message>\d+)/$', views.index, name='index'),
    url(r'search',views.search_titles,name='search_titles'),
    path(r'getPlaces', views.serch_places, name='serch_places'),  #my code for search place
    url(r'admincall',views.admin_search_titles,name='admincall'),
    path('home/<int:num>/',views.result,name='result'),
    path('adminpanel/<int:num>/',views.admin_result,name='admin_result'),
    path('add_image_data/',views.add_image_data,name="add_image_data"),
    path('search_result',views.result,name='result'),
    path('upload/',views.upload,name='upload'),
    path('',views.home,name='home'),
    path('Insert_data/',views.Insert_data,name='Insert_data'),
    path('AllDatalist/',views.AllDatalist,name='AllDatalist'),
    path('AllDatalist/<int:num>/',views.admin_result,name='admin_result'),
    path('UnApprovedlist/',views.UnApprovedlist,name='UnApprovedlist'),
    path('UnApprovedlist/<int:num>/',views.admin_result,name='admin_result'),
    path('Approvedlist/',views.Approvedlist,name='Approvedlist'),
    path('Approvedlist/<int:num>/',views.admin_result,name='admin_result'),
    url(r'csvUpload/',views.csvUpload,name='csvUpload'),
    url(r'status',views.status,name='status'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)