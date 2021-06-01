from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import SaveAudioForm,PredictAudioForm
from .speech.speech_to_text import Speech_to_text
from .speech.stress_detector import StressDetector
from pydub import AudioSegment
from pydub.silence import split_on_silence

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
            language = request.POST['language']
            output = request.POST['output']
            location = "audio_worker\\saved_files\\" + name + ".wav"
            ofile = open(location, 'wb')
            ofile.write((audio.file.read()))
            ofile.close()
            if language == 'RO':
                message = stt.get_text_RO(location)
            elif language == 'EN':
                message = stt.get_test_EN(location)
            else:
                message = 'Language error'
            if output == '2':
                stress = sd.predict2(location)
            elif output == '4':
                stress = sd.predict4(location)
            else:
                stress = 'Stress detection error'

            return JsonResponse({'message':message,'stress':stress},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message':form.errors},status=status.HTTP_400_BAD_REQUEST)


class PredictMultipleText(APIView):
    def post(self,request):
        form = PredictAudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio = request.FILES['audio']
            name = request.POST['name']
            language=request.POST['language']
            output=request.POST['output']
            location = "audio_worker\\saved_files\\" + name + ".wav"
            ofile = open(location, 'wb')
            ofile.write((audio.file.read()))
            ofile.close()
            sound_file = AudioSegment.from_wav(location)
            st = int(sound_file.dBFS)
            print(st)
            audio_chunks = split_on_silence(sound_file,
                    # split on silences longer than 1000ms (1 sec)
                    min_silence_len=250,

                    # anything under -16 dBFS is considered silence
                    silence_thresh=-55,

                    #keep 200 ms of leading/trailing silence
                    keep_silence=200

                                            )

            stresses={}
            array_stress=[]
            for i, chunk in enumerate(audio_chunks):
                out_file = "audio_worker\\splitAudio\\chunk{0}.wav".format(i)
                print(out_file)
                chunk.export(out_file, format="wav")
                if language=='RO':
                    message=stt.get_text_RO(out_file)
                elif language=='EN':
                    message=stt.get_test_EN(out_file)
                else:
                    message='Language error'
                if output=='2':
                    stress=sd.predict2(out_file)
                elif output=='4':
                    stress=sd.predict4(out_file)
                else:
                    stress='Stress detection error'
                stress_aux={"message":message,"stress":stress}
                array_stress.append(stress_aux)
            stresses["results"]=array_stress
            print(stresses)
            return JsonResponse(stresses, status=status.HTTP_200_OK)

        else:
            return JsonResponse({'message': form.errors}, status=status.HTTP_400_BAD_REQUEST)
