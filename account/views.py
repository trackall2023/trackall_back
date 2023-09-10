from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, parsers, status
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import CreateAccountSerializer, CustomAccountSerializer, RetrieveUpdateDestroyAccountSerializer, LoginAccountSerializer, SendPasswordResetEmailSerializer,UserPasswordResetSerializer

from account.models import Custom_User



# Create your views here.


def get_token_for_user(user):
    """
       This function use to get token for User when he is registering
       :param user: (user: Any)
       :return:  dict[str, str]
       """
    refresh = RefreshToken.for_user(user)

    return  {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

#Define custom view to create user account
@authentication_classes([])
class CreateAccountView(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = CreateAccountSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    def post(self, request, *args, **kwargs):
        """
               We redefine the post function for UserRegistrationView.It's being used to  save a new user register
               :param request:
               :param args:
               :param kwargs:
               :return:

             """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # Save user with validated_data without password2 field
                print("we are here")
                user = serializer.save()
                print(serializer)
                print(user)
                return Response({"msg": "Registration successful","user": f'{user}'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


#Define custom view to login user account
@authentication_classes([])
class loginAccountView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginAccountSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    @swagger_auto_schema(
        operation_description="Endpoint Login",
        request_body=LoginAccountSerializer
    )

    def post(self,request):
        serializer = LoginAccountSerializer(data=request.data)

        try:
            print(serializer)
            telephone = request.data.get('telephone')
            password = request.data.get('password')
            try:
                user = Custom_User.objects.get(telephone=telephone)
                if check_password(password, user.password):
                    token = get_token_for_user(user)
                    return Response({'token': token, 'msg': 'Login Sucess'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error':'wrong password'},status=status.HTTP_400_BAD_REQUEST)
            except Custom_User.DoesNotExist:
                return Response({'error': f"This user does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)





# Retrieve Update and Destroy Account View
class RetrieveUpdateDestroyAccountView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveUpdateDestroyAccountSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    queryset = Custom_User.objects.all()




#Get email to reset password view
class SendPasswordResetEmailView(APIView):
    serializer_class = SendPasswordResetEmailSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    @swagger_auto_schema(
        operation_description="Endpoint Login",
        request_body=SendPasswordResetEmailSerializer

    )
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': "Password Reset Sucessfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Reset password
class UserPasswordResetView(APIView):
    serializer_class = UserPasswordResetSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    @swagger_auto_schema(
        operation_description="Changement de password",
        request_body=UserPasswordResetSerializer
    )
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, "token": token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': "Password Reset Sucessfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)