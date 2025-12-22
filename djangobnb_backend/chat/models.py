import uuid

from django.db import models

from useraccount.models import User


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(default='')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='received_messages', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
