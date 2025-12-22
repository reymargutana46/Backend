from rest_framework import serializers

from .models import Conversation, ConversationMessage

from useraccount.serializers import UserDetailSerializer


class ConversationListSerializer(serializers.ModelSerializer):
    users = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'updated_at',)


class ConversationMessageSerializer(serializers.ModelSerializer):
    created_by = UserDetailSerializer(read_only=True, many=False)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'body', 'created_by', 'created_at')


class ConversationDetailSerializer(serializers.ModelSerializer):
    users = UserDetailSerializer(many=True, read_only=True)
    messages = ConversationMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'messages', 'created_at', 'updated_at',)
