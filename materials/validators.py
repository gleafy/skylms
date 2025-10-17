from rest_framework import serializers

def validate_youtube_url(value):
    if value and "youtube.com" not in value and "youtu.be" not in value:
        raise serializers.ValidationError("Ссылка должна вести на YouTube")