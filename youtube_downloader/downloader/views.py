from django.shortcuts import render
from django.http import HttpResponse , FileResponse , JsonResponse
from pytube.exceptions import VideoUnavailable
from pytube import YouTube , Stream
import os
from django.conf import settings
from moviepy.editor import VideoFileClip


def download(request):
  return render(request , 'downloader.html')

def get_video_properties(request):
  if request.method == 'POST':
    link = request.POST['link']
    try:
      video = YouTube(link)
      streams = []
      for stream in video.streams:
        if stream.resolution:
          streams.append({
            'resolution': stream.resolution,
          })
      # Select the stream with the highest resolution
      stream = max((s for s in video.streams if s.resolution), key=lambda s: s.resolution, default=None)
      if stream is None:
        return JsonResponse({
          'error': 'No streams available',
        })  
      quality = stream.resolution
      # Download the video and get the filename
      filename = stream.download(output_path=os.path.join(settings.MEDIA_ROOT, quality))
      # Check if the file exists
      if os.path.exists(filename):
        # Save the filename in the session
        request.session['filename'] = filename
        request.session['quality'] = quality
        # Get available streams and their properties
        # Get video properties
        title = video.title
        duration = video.length
        thumbnail_url = video.thumbnail_url
        quality = quality
        
        # Return a JSON response
        return JsonResponse({
          'title': title,
          'duration': duration,
          'thumbnail_url': thumbnail_url,
          'quality' : quality ,
          'streams': streams,
        })
      else:
        return JsonResponse({
          'error': 'Video file does not exist',
        })
    except VideoUnavailable:
      return JsonResponse({
        'error': 'The requested video is unavailable',
      })

def download_video(request):
  quality = request.session.get('quality')
  print(quality)
  filename = request.session.get('filename')
  if quality is None or filename is None:
    return JsonResponse({'error': 'No video quality or filename has been set yet'})
  # Use the quality to determine the correct filepath
  filepath = os.path.join(settings.MEDIA_ROOT, quality, filename)
  try:
    # Open the file in read mode
    file = open(filepath, 'rb')
    # Create a FileResponse instance and return it
    response = FileResponse(file, as_attachment=True)
    return response
  except FileNotFoundError:
    return JsonResponse({'error': 'The requested video file does not exist'})

def video_to_audio(request):
  filename = request.session.get('filename')
  if filename is None:
    return JsonResponse({'error' : 'No video filename has been set yet'})
  video_clip = VideoFileClip(filename)
  audio_clip = video_clip.audio
  audio_filename = filename.rsplit(".", 1)[0] + ".mp3"
  audio_clip.write_audiofile(audio_filename)   
  request.session['audio_filename'] = audio_filename
  audiopath = os.path.join(settings.MEDIA_ROOT , audio_filename)
  try:
    # Open the file in read mode
    file = open(audiopath, 'rb')
    # Create a FileResponse instance and return it
    response = FileResponse(file, as_attachment=True)
    return response
  except FileNotFoundError:
    return JsonResponse({'error': 'The requested video file does not exist'})