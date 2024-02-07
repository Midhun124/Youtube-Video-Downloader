from django.urls import path
from .  import views

urlpatterns = [
  path('' , views.download , name='download') ,
  path('get_video_properties/' , views.get_video_properties , name='get_video_properties') ,
  path('download_video/' , views.download_video , name='download_video') ,
  path('video_to_audio/' ,views.video_to_audio , name='video_to_audio') ,
]