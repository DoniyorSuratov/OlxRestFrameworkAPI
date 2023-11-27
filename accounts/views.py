from django.contrib.auth.views import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import SellMessages, BuyMessage, UsingResetEmail
from .serializers import SellMessagesSerializer, BuyMessagesSerializer, UserSerializer, UserDataSerializer, \
    PasswordResetSerializer
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from main.tasks import send_email_reset


User = get_user_model()


class RegisterAPIView(APIView):

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        username = request.data.get('username')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return Response({'success': False, 'error': 'Username already exists!'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'error': 'Email already exists! '}, status=400)
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password1
                )

                user_serializer = UserSerializer(user)
                return Response({'success': True, 'data': user_serializer.data})
        else:
            return Response({'success': False, 'error': 'Passwords are not common! '})


class UserInfoAPIView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({'success': True, 'data': user_serializer.data})


class UserMessageSellAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        messages = SellMessages.objects.all()
        messages_data = SellMessagesSerializer(messages, many=True)
        if messages_data.data:
            return Response({'success': True, 'data': messages_data.data})
        return Response({'success': False}, status=404)

    def post(self, request):
        user = request.user
        message = request.data.get('message')
        message = SellMessages.objects.create(
            user=user,
            message=message
        )
        message.save()
        messages_serializer = SellMessagesSerializer(message)
        return Response(messages_serializer.data)


class BuyMessagesAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        message = BuyMessage.objects.all()
        message_data = BuyMessagesSerializer(message, many=True)
        return Response({'success': True, 'data': message_data.data})

    def post(self, request):
        user = request.user
        message = request.data.get('message')
        messages = BuyMessage.objects.create(
            user=user,
            message=message
        )
        messages.save()
        message_serializer = BuyMessagesSerializer(messages)
        return Response(message_serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"succes": "Loged out"}, status=status.HTTP_204_NO_CONTENT)


class LogoutFromAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(
                token=token)  # (t == <BlacklistedToken: Blacklisted token for user>,)  === > _ ==  False or true
        return Response({"succes": "All sessions loged out"}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = UserDataSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)


            send_email_reset.delay(
                email,
                uid,
                token,


            )

            return Response({'detail': 'Password reset link sent to your email.'}, status=202)
        else:
            return Response({'detail': 'Email not found.'}, status=404)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uidb64 = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uidb64)

            if default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password', '')
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password reset successful.'}, status=200)
            else:
                return Response({'detail': 'Invalid token.'}, status=400)
        except Exception as e:
            return Response({'detail': f'{e}.'}, status=400)

