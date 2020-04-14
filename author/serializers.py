from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Passion

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='profile.image', required=False)
    passion = serializers.CharField(source='profile.passion.name', required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'passion', 'image')
        read_only_fields = ('email',)

    def _get_passion(self, name):
        try:
            return Passion.objects.get(name=name)
        except Passion.DoesNotExist:
            return None

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile', {})
        instance.profile.image = profile.get('image', instance.profile.image)
        instance.profile.passion = self._get_passion(profile.get('passion', {}).get('name'))
        instance.profile.save()
        return super().update(instance, validated_data)


class FollowSerializer(serializers.Serializer):
    followee = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    follow_type = serializers.ChoiceField(choices=['follow', 'unfollow'])

    class Meta:
        fields = ('followee',)

    def validate_followee(self, followee):
        if followee == self.context['request'].user:
            raise serializers.ValidationError('"followee" must not be logged-in user')
        return followee

    def follow(self):
        logged_in_user = self.context['request'].user
        logged_in_user.profile.following.add(self.validated_data['followee'].profile)
        return True

    def unfollow(self):
        logged_in_user = self.context['request'].user
        logged_in_user.profile.following.remove(self.validated_data['followee'].profile)
        return True
