from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.views import APIViewMixin
from author.models import SignUpFlow
from rest_auth.registration import views as rest_registration_views


class RegisterView(rest_registration_views.RegisterView):
    def get_object(self):
        try:
            return SignUpFlow.objects.get(temp_token=self.request.data.get('temp_token', 'foo'))
        except SignUpFlow.DoesNotExist:
            raise NotFound(detail='temp_token missing or invalid')

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        fields = ['first_name', 'last_name', 'email', 'image']
        data = {field: getattr(instance, field) for field in fields}
        data.update({'passion': request.data.get('passion'), 'password1': instance.password, 'password2': instance.password})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class RegistrationFlowAPI(APIView, APIViewMixin):

    def get_serializer_klass(self):
        from author.auth import serializers
        step = self.kwargs['step_no']
        return getattr(serializers, f'RegistrationSerializerStep{step}')

    def get_object(self):
        try:
            return SignUpFlow.objects.get(temp_token=self.request.data.get('temp_token', 'foo'))
        except SignUpFlow.DoesNotExist:
            raise NotFound(detail='temp_token missing or invalid')

    def post(self, request, step_no, *args, **kwargs):
        if step_no not in [1, 2, 3, 4]:
            return Response({'detail': 'invalid step'})
        ctx = self.get_serializer_context()
        if step_no == 1:
            serializer = self.get_serializer_klass()(data=request.data, context=ctx)
        else:
            serializer = self.get_serializer_klass()(self.get_object(), data=request.data, context=ctx)
        serializer.is_valid(True)
        instance = serializer.save()
        return Response({'temp_token': instance.temp_token})
