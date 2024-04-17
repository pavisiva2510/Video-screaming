
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import authenticate,login
from django.http import StreamingHttpResponse
from django.contrib.auth.models import User
from .models import Video
from .forms import VideoForm
import cv2
import threading

def stream_video(video_id):
    video = get_object_or_404(Video, pk=video_id)
    cap = cv2.VideoCapture(video.video_file.path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

def video_stream_view(request, video_id):
    return StreamingHttpResponse(stream_video(video_id), content_type='multipart/x-mixed-replace; boundary=frame')

def main_page(request):
    videos = Video.objects.all()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = VideoForm()
    return render(request, 'main_page.html', {'videos': videos, 'form': form})

def edit_video(request, video_id):
    video = get_object_or_404(Video,pk=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = VideoForm(instance=video)
    return render(request, 'edit_video.html', {'form': form})

def delete_video(request, video_id):
    video = get_object_or_404(Video,pk=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('main_page')
    return render(request, 'confirm_delete.html', {'video':video})

def search_videos(request):
    query=request.GET.get('search_query')
    if query:
        videos= Video.objects.filter(name__icontains=query)
    else:
        videos= Video.objects.all()
    return render(request, 'search_results.html', {'videos': videos})

def SignupPage(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
        # Create a new user
        #user = User.objects.create_user(username=username, email=email, password=password)
        if password!=password_repeat:
            return HttpResponse("Your password and comfort password are not same")
        else:
            my_user=User.objects.create_user(username, email, password)
            my_user.save()
        # Log in the user after registration (optional)
        #login(request, user)
            return redirect('login')  # Redirect to the home page after successful signup

    return render(request, 'signup.html')
def  LoginPage(request):
    if request. method == "POST":
        username = request. POST['username']
        password = request. POST['password']
    
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)

            return redirect('main_page')
        else:
            return redirect('signup')
    return render(request,'login.html', {'error': 'Invalid credentials'})

