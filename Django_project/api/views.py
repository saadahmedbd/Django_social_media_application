from rest_framework.decorators import api_view
from  rest_framework.response import Response
# from django.http import JsonResponse

from user.models import Room
from .serilizer import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET/api',
        'Get/api/rooms',
        'Get/api/rooms/:id',
    ]
    return Response (routes)

@api_view(['GET'])
def getRooms (request):
    rooms=Room.objects.all()
    serializer =RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom (request,pk):
    room=Room.objects.get(id=pk)
    serializer =RoomSerializer(room, many=False)
    return Response(serializer.data)