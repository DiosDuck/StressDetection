import librosa
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

class StressDetector:
    # DataFlair - Extract features (mfcc, chroma, mel) from a sound file
    def __extract_feature(self,file_name, mfcc=True, chroma=True, mel=True):
        with soundfile.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate
            if chroma:
                stft = np.abs(librosa.stft(X))
            result = np.array([])
            if mfcc:
                mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
                result = np.hstack((result, mfccs))
            if chroma:
                chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
                result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
        return result

    def __load_data(self,test_size=0.2):
        emotions = {
            '01': 'neutral',
            '02': 'calm',
            '03': 'happy',
            '04': 'sad',
            '05': 'angry',
            '06': 'fearful',
            '07': 'disgust',
            '08': 'surprised'
        }
        observed_stress = ['sad', 'angry', 'fearful']
        x, y = [], []
        for file in glob.glob("audio_worker\\speech\\speech-emotion-recognition-ravdess-data\\Actor_*\\*.wav"):
            file_name = os.path.basename(file)
            emotion = emotions[file_name.split("-")[2]]
            if emotion in observed_stress:
                stress = "True"
            else:
                stress = "False"
            '''if emotion not in observed_emotions:
                continue
                '''
            feature = self.__extract_feature(file, mfcc=True, chroma=True, mel=True)
            x.append(feature)
            y.append(stress)
        return train_test_split(np.array(x), y, test_size=test_size, random_state=9)

    def __fit(self):
        # DataFlair - Split the dataset
        x_train, x_test, y_train, y_test = self.__load_data(test_size=0.2)
        self.__scaler = StandardScaler()
        self.__scaler.fit(x_train)
        x_train = self.__scaler.transform(x_train)

        # DataFlair - Initialize the Multi Layer Perceptron Classifier
        self.__model = MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-09, hidden_layer_sizes=(300,),
                              learning_rate='adaptive', max_iter=500)

        # DataFlair - Train the model
        self.__model.fit(x_train, y_train)


    def __init__(self):
        self.__fit()

    def predict(self,file):
        x=self.__scaler.transform([self.__extract_feature(file)])
        return self.__model.predict(x)[0]