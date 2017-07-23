from rest_framework import routers, serializers, viewsets

from channel.models import Video, Channel

from django.contrib.auth.models import User

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'

class ChannelSerializer(serializers.ModelSerializer):

    content = VideoSerializer(many=True,read_only=True)

    class Meta:
        model = Channel
        fields = ('name','content','user')

class UserSerializer(serializers.ModelSerializer):

    channels = ChannelSerializer(many=True,read_only=True)

    class Meta:
        model = User
        fields = ('id','username','channels')
