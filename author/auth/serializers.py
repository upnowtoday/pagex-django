from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_auth import serializers as auth_serializers
from rest_auth.registration import serializers as registration_serializers
from author.models import SignUpFlow

User = get_user_model()


class PasswordResetSerializer(auth_serializers.PasswordResetSerializer):
    def get_email_options(self):
        opts = {
            'from_email': settings.PASSWORD_RESET_FROM_EMAIL,

        }
        try:
            opts['email_template_name'] = settings.PASSWORD_RESET_CONFIRM_TEMPLATE_NAME
        except AttributeError:
            pass
        return opts


class RegisterSerializer(registration_serializers.RegisterSerializer):
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25, allow_blank=True)
    passion = serializers.CharField(required=True)
    image = serializers.ImageField(required=False)

    def get_passion(self):
        from author.models import Passion
        try:
            passion, created = Passion.objects.get_or_create(name=self.validated_data['passion'])
            return passion
        except KeyError:
            return None

    def get_image(self):
        return self.validated_data.get('image')

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data

    def save(self, request):
        from author.models import Profile
        user = super().save(request)
        profile = Profile.objects.create(user=user, passion=self.get_passion())
        image = self.get_image()
        profile.image.save(image.name.split('/')[-1], image)

        return user


class RegistrationSerializerStep1(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'email already exists'})
        return email

    def create(self, validated_data):
        instance, created = SignUpFlow.objects.get_or_create(**validated_data)
        instance.generate_code()
        instance.generate_temp_token()
        return instance


class RegistrationSerializerStep2(serializers.Serializer):
    code = serializers.CharField(allow_null=False, required=True)

    def validate_code(self, code):
        if self.instance.code == code:
            return code
        raise serializers.ValidationError('invalid code')

    def update(self, instance, validated_data):
        instance.is_code_verified = True
        instance.save()
        return instance


class RegistrationSerializerStep3(serializers.Serializer):
    password = serializers.CharField(min_length=8)

    def update(self, instance, validated_data):
        instance.password = validated_data['password']
        instance.save()
        return instance


class RegistrationSerializerStep4(serializers.Serializer):
    image = serializers.ImageField()

    def update(self, instance, validated_data):
        instance.image = validated_data['image']
        instance.save()
        return instance
