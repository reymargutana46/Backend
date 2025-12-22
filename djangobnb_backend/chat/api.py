from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Conversation
from .serializers import ConversationListSerializer, ConversationDetailSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations_list(request):
    serializer = ConversationListSerializer(
        request.user.conversations.all(), many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_detail(request, pk):
    try:
        conversation = request.user.conversations.get(pk=pk)
        serializer = ConversationDetailSerializer(conversation, many=False)
        return Response(serializer.data)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
