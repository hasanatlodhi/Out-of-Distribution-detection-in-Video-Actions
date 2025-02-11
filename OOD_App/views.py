from django.shortcuts import render
from django.http.response import HttpResponse
from urllib.request import Request, urlopen
import os
import json
from django.http import JsonResponse
from omegaconf import OmegaConf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import uuid
# from pytube import YouTube 
from .action_recognition import predict_on_video
from .i3d_action_recognition import I3DModel
from tensorflow.keras.models import Sequential,load_model
from .main import main
from django.http import StreamingHttpResponse
import time
import json
import numpy as np
import tempfile
import cv2
from django.conf import settings
from .models import ContactMessage
from moviepy.video.io.VideoFileClip import VideoFileClip
options=webdriver.ChromeOptions()
options.headless = True
# Create your views here.
import yt_dlp


def index_page(request):
    return render(request,"index.html")

def login_page(request):
    return render(request,"login.html")

def our_team(request):
    return render(request,"Ourteam.html")

def blogs(request):
    return render(request,"Blogs.html")
def contact(request):
    return render(request,"ContactUs.html")

def upload_video(request):
    if request.method=="POST":
        video=request.FILES['video_file']
        extension=str(video).split('.')[1]
        file_name=str(uuid.uuid4())[:8]
        with open(f'{os.getcwd()}/static/videos/{file_name}.{extension}', 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)
    # predict_on_video(f'{os.getcwd()}/static/videos/{file_name}.{extension}',f'{os.getcwd()}/static/recognizedVideos/{file_name}.mp4')
    
    video_path=f'{os.getcwd()}/static/videos/{file_name}.{extension}'
    args_cli = {'feature_type': 'i3d', 'device': 'cuda:0','stack_size':42,'step_size':42, 'video_paths': [f'{video_path}']}
    args_cli=OmegaConf.create(args_cli)
    rgb_flow=main(args_cli)
    i3d_model=I3DModel()
    actions_dict,actions_with_prob=i3d_model.recognize(rgb_flow,video_path,f'{os.getcwd()}/static/recognizedVideos/{file_name}.mp4')
    my_dict={"all_actions":actions_dict,"actions_prob":actions_with_prob}
    my_dict=json.dumps(my_dict)
    return render(request,"upload_report.html",{"video_path":f"{file_name}","vid_data":my_dict})


def upload_file(request):
    if request.method=="POST":
        links_file=request.FILES.get('links_file')
        if links_file:
            lines = [line.strip().decode("utf-8") for line in links_file]
            dataDictionary={'all_links':lines}
            dataJSON = json.dumps(dataDictionary)
        return render(request,"multiple_reports.html",{"data":dataJSON})


def fetch_video(request):
    return render(request,"report.html",{"video_path":None})

def get_video(request):
    if request.method=="POST":
        link=request.POST.get('url')
        try:
            if "youtube.com" in link:
                file_name=str(uuid.uuid4())[:8]
                # try:
                #     yt = YouTube(link) 
                # except: 
                #     print("Connection Error") #to handle exception 
                # mp4files = yt.streams.filter('mp4')
                # file_name=str(uuid.uuid4())[:8]
                # mp4files[0].download(output_path=os.getcwd()+'/static/videos',filename=f"{file_name}.mp4")
                ydl_opts = {
                    'outtmpl': f'./static/videos/{file_name}.'+'%(ext)s',
                    'format': 'mp4'
                }

                # Create a YoutubeDL object with download options
                ydl = yt_dlp.YoutubeDL(ydl_opts)

                # Define the URL of the video you want to download

                # Download the video
                ydl.download([link])
                return HttpResponse(f"{file_name}.mp4")
            elif 'facebook' in link:
                driver=webdriver.Chrome(os.getcwd()+'/static/drivers/chromedriver.exe',chrome_options=options)
                driver.get("https://snapsave.app/")  
                input_box=driver.find_element("id","url")
                input_box.send_keys(link)  
                print("Please wait downloading your video")
                button=driver.find_element("id",'send')
                button.click()
                # driver.implicitly_wait(5)
                wait = WebDriverWait(driver, 10)
                table = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'tbody')))
                # table=driver.find_element(By.TAG_NAME,'tbody')
                elements=table.find_elements(By.CLASS_NAME,'button')
                href=elements[0].get_attribute('href')
                driver.quit()
                request_site = Request(href, headers={"User-Agent": "Mozilla/5.0"})
                webpage = urlopen(request_site).read()
                print("Here it is done")
                file_name=str(uuid.uuid4())[:8]
                out_file = open(f"{os.getcwd()}/static/videos/{file_name}.mp4", "wb") # open for [w]riting as [b]inary
                out_file.write(webpage)
                out_file.close()
                return HttpResponse(f"{file_name}.mp4")
            else:
                return HttpResponse("error")
        except Exception as e:
             print("Exceptio:  ",e)
             return HttpResponse("unable")

def recognize_action_LRCN(request):
    video_name=request.POST.get('video_name')
    extension=str(video_name).split('.')[1]
    file_name=str(video_name).split('.')[0]
    predict_on_video(f'{os.getcwd()}/static/videos/{file_name}.{extension}',f'{os.getcwd()}/static/recognizedVideos/{file_name}.mp4')
    return HttpResponse(f"{file_name}.mp4")



# I3d work starts here

def convert_to_seconds(points):
    minutes = int(points)
    seconds = int((points % 1) * 100)
    total_seconds = (minutes * 60) + seconds
    return total_seconds

def trim_video(input_path, output_path, start_time, end_time):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    total_frames = end_frame - start_frame
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frame_count = start_frame
    
    while cap.isOpened() and frame_count <= end_frame:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        
        out.write(frame)
        frame_count += 1
    
    cap.release()
    out.release()


def recognize_longer_vid_using_i3d(request):

    video_name=request.POST.get('video_name')
    extension=str(video_name).split('.')[1]
    file_name=str(video_name).split('.')[0]
    video_path=f'{os.getcwd()}/static/videos/{file_name}.{extension}'
    output_path = f'{os.getcwd()}/static/videos/{file_name}.{extension}'
    last_vid=request.POST.get('last_vid')
    start_time=int(request.POST.get('start_time'))
    end_time=int(request.POST.get('end_time'))
    vid_duration=request.POST.get('video_length')
    next=int(request.POST.get('next_video'))

    trim_video(video_path,output_path,start_time,end_time)
    
    
    args_cli = {'feature_type': 'i3d', 'device': 'cuda:0','stack_size':42,'step_size':42, 'video_paths': [f'{output_path}']}
    args_cli=OmegaConf.create(args_cli)
    rgb_flow=main(args_cli)
    i3d_model=I3DModel()
    actions_dict,actions_with_prob=i3d_model.recognize(rgb_flow,output_path,f'{os.getcwd()}/static/recognizedVideos/{file_name}_{next}.mp4')
    if next>0:
        concatenate_videos(f'{os.getcwd()}/static/recognizedVideos/{last_vid}.mp4',f'{os.getcwd()}/static/recognizedVideos/{file_name}_{next}.mp4',f'{os.getcwd()}/static/recognizedVideos/{file_name}Added{next}.mp4')
        last_vid=f'{file_name}Added{next}'
    else:
        last_vid=f'{file_name}_{next}'
        
    my_dict={'file_name':f"{last_vid}.mp4","all_actions":actions_dict,"actions_prob":actions_with_prob,"last_vid":last_vid}
    my_dict=json.dumps(my_dict)
    return HttpResponse(my_dict)



def concatenate_videos(video1_path, video2_path, output_path):
    # Open the first video file
    video1 = cv2.VideoCapture(video1_path)
    fps = video1.get(cv2.CAP_PROP_FPS)
    width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Open the second video file
    video2 = cv2.VideoCapture(video2_path)

    # Define the codec and VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Read and write frames from the first video
    while video1.isOpened():
        ret, frame = video1.read()

        if not ret:
            break

        out.write(frame)

    # Read and write frames from the second video
    while video2.isOpened():
        ret, frame = video2.read()

        if not ret:
            break

        out.write(frame)

    # Release the resources
    video1.release()
    video2.release()
    out.release()

    print("Videos concatenated successfully.")



def recognize_using_i3d(request):
    video_name=request.POST.get('video_name')
    extension=str(video_name).split('.')[1]
    file_name=str(video_name).split('.')[0]
    video_path=f'{os.getcwd()}/static/videos/{file_name}.{extension}'
    output_path = f'{os.getcwd()}/static/videos/{file_name}_trimmed.{extension}'

    start_time=request.POST.get('start_time')
    start_time=convert_to_seconds(float(start_time))
    end_time=request.POST.get('end_time')
    end_time=convert_to_seconds(float(end_time))
    vid_duration=request.POST.get('video_length')
    vid_duration=convert_to_seconds(float(vid_duration))
    
    print("\n\nResult: ",start_time,end_time)

    trim_video(video_path,output_path,start_time,end_time)
    
    
    args_cli = {'feature_type': 'i3d', 'device': 'cuda:0','stack_size':64,'step_size':64, 'video_paths': [f'{output_path}']}
    args_cli=OmegaConf.create(args_cli)
    rgb_flow=main(args_cli)
    print("RRRHGGBBBBB:   ",rgb_flow)
    print("\n\n\nReachedHere\n\n\n\n")
    i3d_model=I3DModel()
    actions_dict,actions_with_prob=i3d_model.recognize(rgb_flow,output_path,f'{os.getcwd()}/static/recognizedVideos/{file_name}.mp4')
    print("This is: ",actions_with_prob)
    my_dict={'file_name':f"{file_name}.mp4","all_actions":actions_dict,"actions_prob":actions_with_prob}
    my_dict=json.dumps(my_dict)
    return HttpResponse(my_dict)

def download_segment(request):
    video_name=request.POST.get('video_name')
    start_time = float(request.POST.get("start_time"))
    end_time = round(float(request.POST.get("end_time")),2)
    file_name=str(video_name).split('.')[0]
    video_path = f'{os.getcwd()}/static/recognizedVideos/{file_name}.mp4'
    video = VideoFileClip(video_path)
    segment = video.subclip(start_time, end_time)
    file_name=str(uuid.uuid4())[:8]
    segment.write_videofile(f'{os.getcwd()}/static/extracted_segments/{file_name}.mp4')
    my_dict={"fileName":f"{file_name}.mp4"}
    my_dict=json.dumps(my_dict)
    return HttpResponse(my_dict)

def search_yt(request):
    return render(request,"search_yt.html")

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('firstname')
        name = name+" "+request.POST.get('lastname')
        email = request.POST.get('emailaddress')
        message = request.POST.get('usermessage')
        
        contact_message = ContactMessage(user_name=name, email=email, message=message)
        contact_message.save()

        return HttpResponse("success")
    else:
        return HttpResponse("error")