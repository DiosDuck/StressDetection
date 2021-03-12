import speech_recognition as sr

class Speech_to_text:
    def __init__(self):
        self.__r=sr.Recognizer()

    def get_text(self,file):
        f=sr.AudioFile(file)
        with f as source:
            self.__r.adjust_for_ambient_noise(source)
            audio = self.__r.record(source)

        return self.__r.recognize_google(audio)

