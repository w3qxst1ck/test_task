from rest_framework import serializers

from comments.models import Comment


class CreateCommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'text', 'parent', 'is_child']


class UpdateCommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']
