from django.urls import path
from . import views

urlpatterns=[
  
    path('',views.index_page),
    path('login',views.login_page),
    path('blogs',views.blogs),
    path('contactus',views.contact),
    path('fetch_video',views.fetch_video),
    path('recognize_action',views.recognize_action_LRCN),
    path('recognize_i3d',views.recognize_using_i3d),
    path('get_video',views.get_video),
    path('upload_video',views.upload_video),
    path('upload_file',views.upload_file),
    path('ourteam',views.our_team),
    path('download_segment',views.download_segment),
    path('search_yt',views.search_yt),
    path('longer_recognize', views.recognize_longer_vid_using_i3d),
    path('contactadmin', views.contact_us),
]