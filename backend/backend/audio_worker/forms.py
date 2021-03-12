from django import forms

class SaveAudioForm(forms.Form):
    name = forms.CharField(max_length=50)
    audio = forms.FileField()

class PredictAudioForm(forms.Form):
    name = forms.CharField(max_length=50)
    audio = forms.FileField()