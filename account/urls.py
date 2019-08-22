from django.conf.urls import url
from django.urls import include
from rest_framework.authtoken import views as rest_framework_views

from account import views

urlpatterns = [
    url(r'^registration/$', views.CreateUserView.as_view()),
    url(r'^check/email/$', views.is_email_taken),
    url(r'^check/username/$', views.is_username_taken),
    url(r'^recovery/$', views.password_recovery),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^info/change/$', views.AccountUpdate.as_view()),
    url(r'^todo/delay/change/$', views.ProfileUpdate.as_view()),
]

urlpatterns += [
    url(r'^auth/', include('rest_framework.urls')),
]