# in this urls.py - import this function hello
# then associate this fn with the URL

from django.urls import path

#  import from api/views.py file
from .views import hello

#  associate the path -> function
urlpatterns=[
    path("hello/",hello)
]

#  what will happen as django run on localhost:8000 ->  on localhost:8000//hello/ run this hello fn when it'S A GET CALL

# every app should have it's own urls.py file

#  api App -> urls.py

#  but project should be able to identify ok this URL pattern --> (mapped to) App
# register app/urls.py routes of a single app -> project level congif/urls.py file


# In a Django Project, a sigle App can have multiple URL patterns/ routes in it's urls.py, each pointing to a view.
