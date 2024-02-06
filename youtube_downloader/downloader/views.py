from django.shortcuts import render
from django.http import HttpResponse , FileResponse
from pytube.exceptions import VideoUnavailable
from pytube import YouTube
import os


def download(request):
  return render(request , 'downloader.html')

def get_video_properties(request):
  if request.method == 'POST':
    link = request.POST['link']
    try:
      video = YouTube(link)
      stream = video.streams.get_highest_resolution()
      # Download the video and get the filename
      filename = stream.download(output_path=settings.MEDIA_ROOT)
      # Check if the file exists
      if os.path.exists(filename):
        # Save the filename in the session
        request.session['filename'] = filename
        # Get available streams and their properties
        # Get video properties
        title = video.title
        duration = video.length
        thumbnail_url = video.thumbnail_url
        quality = stream.resolution
        # Return a JSON response
        return JsonResponse({
          'title': title,
          'duration': duration,
          'thumbnail_url': thumbnail_url,
          'quality': quality,
        })
      else:
        return JsonResponse({
          'error': 'Video file does not exist',
        })
    except VideoUnavailable:
      return JsonResponse({
        'error': 'The requested video is unavailable',
      })