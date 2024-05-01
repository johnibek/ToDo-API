from django.http import Http404
from .serializers import ToDoSerializer
from rest_framework.decorators import api_view, permission_classes
from .models import Todo, CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import AuthorEditPermission

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def todo_list_view(request):
    if request.method == 'GET':
        todo_items = Todo.objects.all()
        serializer = ToDoSerializer(todo_items, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, AuthorEditPermission])
def todo_detail_view(request, id):
    try:
        todo_item = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = ToDoSerializer(todo_item, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = ToDoSerializer(todo_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        todo_item.delete()
        return Response({'message': "You have successfully deleted your todo item"}, status.HTTP_200_OK)

