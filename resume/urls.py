from django.urls import path
from .views import Index,NewContact


app_name='resume'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('NewContact/', NewContact.as_view(), name='newcontact'),
]
