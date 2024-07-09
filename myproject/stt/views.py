# import os
# import json
# import base64
# import wave
# import pyaudio
# import threading
# import queue
# import urllib3
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.shortcuts import render

# def index(request):
#     return render(request, 'index.html')

# # 설정
# CHUNK = 1024  # 버퍼 크기
# FORMAT = pyaudio.paInt16  # 음성 포맷
# CHANNELS = 1  # 모노 채널
# RATE = 16000  # 샘플링 레이트
# RECORD_SECONDS = 1  # 녹음 시간 단위 (1초)
# WAVE_OUTPUT_FILENAME = "output.wav"  # 전체 저장할 파일 이름

# # ETRI API 설정
# openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
# accessKey = "2b233e5f-a9c9-4224-989a-5b3d781f3385"
# languageCode = "korean"

# # 전역 변수
# recording = False
# audio_queue = queue.Queue()
# frames = []

# def recognize_with_etri(audio_data):
#     audio_contents = base64.b64encode(audio_data).decode("utf8")
    
#     request_json = {
#         "argument": {
#             "language_code": languageCode,
#             "audio": audio_contents
#         }
#     }
    
#     http = urllib3.PoolManager()
#     response = http.request(
#         "POST",
#         openApiURL,
#         headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
#         body=json.dumps(request_json)
#     )
    
#     response_data = json.loads(response.data.decode("utf-8"))
#     return response_data

# @method_decorator(csrf_exempt, name='dispatch')
# class StartRecordingAPIView(APIView):

#     def post(self, request, *args, **kwargs):
#         global recording
#         if recording:
#             return Response({"error": "Recording is already in progress."}, status=status.HTTP_400_BAD_REQUEST)
        
#         recording = True
        
#         def audio_recorder():
#             p = pyaudio.PyAudio()
#             stream = p.open(format=FORMAT,
#                             channels=CHANNELS,
#                             rate=RATE,
#                             input=True,
#                             frames_per_buffer=CHUNK)
            
#             print("Recording...")
#             try:
#                 while recording:
#                     audio_data = []
#                     for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#                         data = stream.read(CHUNK)
#                         audio_data.append(data)
                    
#                     audio_data = b''.join(audio_data)
#                     frames.append(audio_data)
#                     audio_queue.put(audio_data)
#             except Exception as e:
#                 print("Recording error:", e)
#             finally:
#                 stream.stop_stream()
#                 stream.close()
#                 p.terminate()
#                 audio_queue.put(None)
        
#         def process_audio():
#             while True:
#                 audio_data = audio_queue.get()
#                 if audio_data is None:
#                     break
                
#                 response = recognize_with_etri(audio_data)
#                 if response.get('result') == 0:
#                     text = response['return_object']['recognized']
#                     print("Recognized text: ", text)
#                 else:
#                     print("Error recognizing audio with ETRI API")
        
#         recording_thread = threading.Thread(target=audio_recorder)
#         processing_thread = threading.Thread(target=process_audio)
        
#         recording_thread.start()
#         processing_thread.start()
        
#         return Response({"message": "Recording started."}, status=status.HTTP_200_OK)

# @method_decorator(csrf_exempt, name='dispatch')
# class StopRecordingAPIView(APIView):

#     def post(self, request, *args, **kwargs):
#         global recording, frames
#         if not recording:
#             return Response({"error": "Recording is not in progress."}, status=status.HTTP_400_BAD_REQUEST)
        
#         recording = False
#         # 전체 녹음 데이터 저장
#         with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
#             wf.setnchannels(CHANNELS)
#             wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
#             wf.setframerate(RATE)
#             wf.writeframes(b''.join(frames))
        
#         # frames 초기화
#         frames = []
#         return Response({"message": "Recording stopped and saved as " + WAVE_OUTPUT_FILENAME}, status=status.HTTP_200_OK)


import os
import pyaudio
import wave
import threading
import requests
import time
import queue
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# 네이버 클로바 스피치 API 설정
client_id = "etu7ckegx5"
client_secret = "4WtVsc9mDlMZJmsrswHcZIaOlW2Fz200DMAmEFvO"
lang = "Kor"  # 언어 코드 (한국어: Kor)
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

# 오디오 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5  # 클로바 스피치용 녹음 길이 (초)
WAVE_OUTPUT_FILENAME_1 = "output1.wav"
WAVE_OUTPUT_FILENAME_2 = "output2.wav"
FULL_CONVERSATION_FILENAME = "full_conversation.wav"

# PyAudio 초기화
audio = pyaudio.PyAudio()

# 오디오 큐 초기화
audio_queue_1 = queue.Queue()
audio_queue_2 = queue.Queue()

# 전역 변수
recording = False

def recognize_speech(file_path):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }
    with open(file_path, 'rb') as data:
        response = requests.post(url, data=data, headers=headers)
    rescode = response.status_code
    if rescode == 200:
        print("Recognized text:", response.text)
    else:
        print("Error:", response.text)

def continuous_recording():
    global recording
    wf_full = wave.open(FULL_CONVERSATION_FILENAME, 'wb')
    wf_full.setnchannels(CHANNELS)
    wf_full.setsampwidth(audio.get_sample_size(FORMAT))
    wf_full.setframerate(RATE)

    def callback(in_data, frame_count, time_info, status):
        if not recording:
            return in_data, pyaudio.paComplete
        wf_full.writeframes(in_data)
        if audio_queue_1.qsize() <= audio_queue_2.qsize():
            audio_queue_1.put(in_data)
        else:
            audio_queue_2.put(in_data)
        return in_data, pyaudio.paContinue

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=callback)

    print("Recording...")
    stream.start_stream()

    while recording:
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    wf_full.close()

def periodic_recognition(queue, output_filename):
    while recording or not queue.empty():
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if not recording and queue.empty():
                break
            frames.append(queue.get())

        if frames:
            wf = wave.open(output_filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            recognize_speech(output_filename)
            time.sleep(1)

def index(request):
    return render(request, 'index.html')

@method_decorator(csrf_exempt, name='dispatch')
class StartRecordingAPIView(View):
    def post(self, request, *args, **kwargs):
        global recording
        if recording:
            return JsonResponse({"error": "Recording is already in progress."}, status=400)

        recording = True

        record_thread = threading.Thread(target=continuous_recording)
        recognize_thread_1 = threading.Thread(target=periodic_recognition, args=(audio_queue_1, WAVE_OUTPUT_FILENAME_1))
        recognize_thread_2 = threading.Thread(target=periodic_recognition, args=(audio_queue_2, WAVE_OUTPUT_FILENAME_2))

        record_thread.start()
        recognize_thread_1.start()
        recognize_thread_2.start()

        return JsonResponse({"message": "Recording started."}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class StopRecordingAPIView(View):
    def post(self, request, *args, **kwargs):
        global recording
        if not recording:
            return JsonResponse({"error": "Recording is not in progress."}, status=400)

        recording = False
        return JsonResponse({"message": "Recording stopped."}, status=200)