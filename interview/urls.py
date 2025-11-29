from django.urls import path
from . import views

urlpatterns = [
    path("", views.interview_page, name="home"),
    path("interview/", views.interview_page, name="interview_home"),
    path("start/", views.start_interview, name="start_interview"),
    path("begin/", views.process_interview, name="begin"),  
    path("stop/", views.stop_interview, name="stopInterview"), 
]
