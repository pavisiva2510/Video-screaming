from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/', views.main_page, name='main_page'),
    path('edit/<int:video_id>/', views.edit_video, name='edit_video'),
    path('delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('search/', views.search_videos, name='search_videos'),
    path('video/stream/<int:video_id>/',views.video_stream_view,name='video_stream'),

   ]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)