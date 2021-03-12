from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('start/',views.GetStart.as_view()),
    path('save/',views.SaveFile.as_view()),
    path('predict/',views.PredictAndText.as_view())
]