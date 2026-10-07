from django.http import response
from rest_framework.decorators import api_view
# response class is already present in the framework
from rest_framework.response import Response

# backend : takes a request --> returns a response
# Request: 3 parts -> type, URL & data -> | URL | Data |  are most important

# define type in api_view: Type in request
@api_view(['GET'])

# fn hello is returning an object from response
def hello(request):
    # this response object has many class object fields: data, status, template_name etc.
    
    # Msg -> data in a response
    return Response({"message":"Hello from AirTribe !!"})

# need to define the path: URL -> api/urls.py (new folder)


def add(request):
    # take query parameters -> convert them to int
    a=int(request.query_params.get("a"))
    b=int(request.query_params.get('b'))
    return Response({"Sum of a & b": a+b})