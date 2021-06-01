import librosa
import soundfile
import numpy as np
from .standard_scale import Scale
from .PytorchANN import Net4
import torch
import torch.nn as nn
import torch.nn.functional as F

class StressDetector:
    # DataFlair - Extract features (mfcc, chroma, mel) from a sound file
    def __extract_feature(self,file_name, n_mfcc=20, mfcc_mean=False, mfcc_std=False, chroma_cqt_mean=False,
                        chroma_cqt_std=False,
                        mel_mean=False, mel_std=False, chroma_stft_mean=False, chroma_stft_std=False):
        with soundfile.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate
            result = np.array([])
            if mfcc_mean:
                mfcc_mean = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=n_mfcc).T, axis=0)
                result = np.hstack((result, mfcc_mean))
            if mfcc_std:
                mfcc_std = np.std(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=n_mfcc).T, axis=0)
                result = np.hstack((result, mfcc_std))
            if chroma_stft_mean:
                stft = np.abs(librosa.stft(X))
                chroma_stft_mean = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
                result = np.hstack((result, chroma_stft_mean))
            if chroma_stft_std:
                stft = np.abs(librosa.stft(X))
                chroma_stft_std = np.std(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
                result = np.hstack((result, chroma_stft_std))
            if chroma_cqt_mean:
                cqt = np.abs(librosa.cqt(X))
                chroma_cqt_mean = np.mean(librosa.feature.chroma_cqt(C=cqt, sr=sample_rate).T, axis=0)
                result = np.hstack((result, chroma_cqt_mean))
            if chroma_cqt_std:
                cqt = np.abs(librosa.cqt(X))
                chroma_cqt_std = np.std(librosa.feature.chroma_cqt(C=cqt, sr=sample_rate).T, axis=0)
                result = np.hstack((result, chroma_cqt_std))
            if mel_mean:
                mel_mean = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
                result = np.hstack((result, mel_mean))
            if mel_std:
                mel_std = np.std(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
                result = np.hstack((result, mel_std))
        return result

    def __fit(self):
        #scale
        self.__scale=Scale()
        self.__scale.prebuild(".\\audio_worker\\speech\\utils\\mfcc20cqtall.txt")

        #ann
        self.__ann2=Net4(n=64,o=2)
        self.__ann2.load_state_dict(torch.load(".\\audio_worker\\speech\\utils\\Adam4MFCC20CQTall2.txt"))
        self.__ann4=Net4(n=64,o=4)
        self.__ann4.load_state_dict(torch.load(".\\audio_worker\\speech\\utils\\Adam4MFCC20CQTall4.txt"))

        #labels
        self.__label2=['Stress','No stress']
        self.__label4=['fearful','sad','angry','No stress']

    def __init__(self):
        self.__fit()

    def predict2(self,file):
        x=self.__scale.transform(np.array([self.__extract_feature(file,mfcc_mean=True,mfcc_std=True,chroma_cqt_mean=True,chroma_cqt_std=True)]))
        x=torch.from_numpy(x).type(torch.FloatTensor).view(-1,64)
        return self.__label2[torch.argmax(self.__ann2(x))]

    def predict4(self,file):
        x=self.__scale.transform(np.array([self.__extract_feature(file,mfcc_mean=True,mfcc_std=True,chroma_cqt_mean=True,chroma_cqt_std=True)]))
        x = torch.from_numpy(x).type(torch.FloatTensor).view(-1, 64)
        return self.__label4[torch.argmax(self.__ann4(x))]