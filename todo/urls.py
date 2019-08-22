from django.conf.urls import url

from todo import views

urlpatterns = [
    url(r'^update/$', views.UpdateToDo.as_view()),
]