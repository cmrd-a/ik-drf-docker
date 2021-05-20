from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Entry, Like


class EntrySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Entry
        fields = ['id', 'user', 'text', 'likes']
        read_only_fields = ['id', 'user', 'likes']


class EntryPrivateSerializer(EntrySerializer):
    class Meta(EntrySerializer.Meta):
        fields = EntrySerializer.Meta.fields + ['created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'entry']
        read_only_fields = ['id', 'user']

    def validate(self, data):
        user = self.context['request'].user
        entry = data.get('entry')

        like = Like.objects.filter(user=user, entry=entry).first()
        if like:
            raise serializers.ValidationError('Your like for this post already exists.')

        data['user'] = user
        return super().validate(data)
