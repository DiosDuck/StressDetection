from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import SaveAudioForm,PredictAudioForm
from .speech.speech_to_text import Speech_to_text
from .speech.stress_detector import StressDetector

stt=Speech_to_text()
sd=StressDetector()


def home(request):
    return HttpResponse("Hello World")

class GetStart(APIView):
    def get(self,request):
        return JsonResponse({'name':'success'})

class SaveFile(APIView):
    def post(self,request):
        form=SaveAudioForm(request.POST,request.FILES)
        if form.is_valid():
            audio=request.FILES['audio']
            name=request.POST['name']
            location="audio_worker\\saved_files\\"+name+".wav"
            ofile=open(location,'wb')
            ofile.write((audio.file.read()))
            ofile.close()
            return JsonResponse({'message':'successfully saved'},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message':form.errors},status=status.HTTP_400_BAD_REQUEST)

class PredictAndText(APIView):
    def post(self,request):
        form=PredictAudioForm(request.POST,request.FILES)
        if form.is_valid():
            audio = request.FILES['audio']
            name = request.POST['name']
            location = "audio_worker\\saved_files\\" + name + ".wav"
            ofile = open(location, 'wb')
            ofile.write((audio.file.read()))
            ofile.close()
            message=stt.get_text(location)
            stress=sd.predict(location)
            return JsonResponse({'message':message,'stress':stress},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message':form.errors},status=status.HTTP_400_BAD_REQUEST)