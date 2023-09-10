from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import  models

from account.models import Custom_User
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.utils import Util

# Define a custom serializer for the Custom_User model
class CustomAccountSerializer(serializers.ModelSerializer):

    class Meta:
        # Specify the model to use for the serializer
        model = Custom_User

        # Include all fields from the model in the serialization
        fields = '__all__'


# Define a custom serializer for creating user accounts
class CreateAccountSerializer(serializers.ModelSerializer):

    # Define a custom field for confirming the password
    password2 = serializers.CharField(style={'input_type': "password"}, write_only=True)

    class Meta:
        # Specify the model to use for the serializer
        model = Custom_User

        # Define the fields to include in the serializer
        fields = ['lastname', 'firstname', 'telephone', 'password', 'password2']

        # Specify extra kwargs for fields
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """
        This function is used to validate user input passwords.
        :param attrs: The attributes to validate.
        :return: attrs
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        return attrs

    def create(self, validated_data):
        """
        Used to create a User in the database.
        :param validated_data: The validated data for creating the User.
        :return: User
        """
        password = validated_data.pop('password2')
        user = Custom_User.objects.create_user(**validated_data)

        return user



#Define a custom serirlaizer for login user account
class LoginAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Custom_User
        fields = ['telephone', 'password']


#Define custom serializer for retrieving, updating and delete for user account
class RetrieveUpdateDestroyAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Custom_User
        fields = ['username', 'lastname', 'firstname', 'email', 'telephone', 'adresse', 'sexe', 'birth_date', 'description', 'profession', 'picture']
        extra_kwargs = {'password': {'write_only': True}}



#Define custom serializer for user to ask process to change password when he forget it
class SendPasswordResetEmailSerializer(serializers.Serializer):
    """
    Serilaizer class for user to ask process to change his password when he forget it
    We get it email and send him the token and Uid which help him to change his passord
    """
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = Custom_User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        if Custom_User.objects.filter(email=email).exists:
            user = Custom_User.objects.get(email=email)
            #Encode the uid
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            #reset token for the user
            token = PasswordResetTokenGenerator().make_token(user)
            print(f"tokenn", token)

            #let's send the mail to user
            body = f"\n Uid: {uid} \n Token: {token}"
            data = {
                'subject': "Reset Yout Password ",
                "body": body,
                "to_email": user.email
            }
            Util.send_mail(data)
            #send_mail("Reset Yout Password", "Click this link to change your mail", "oseesoke@gmail.com", [f"{user.email}"])
            return attrs
        else:
            raise ValidationError("Any account associeted to this email")



#Define custom serializer for user to reset password after getting email to do it
class UserPasswordResetSerializer(serializers.Serializer):

    """
        Serializer class to allow user change his password after get the resetpassword mail
    """
    password = serializers.CharField(max_length=255, style={'input_type': "password"}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': "password"}, write_only=True)

    class Meta:
        fields = ['password', "password2"]

    def validate(self, attrs):
       try:
           password = attrs.get('password')
           password2 = attrs.get('password2')
           uid = self.context.get('uid')
           token = self.context.get('token')

           if password != password2:
               raise serializers.ValidationError('Password and Confirm Password doesn\'t match')
           id = smart_str(urlsafe_base64_decode(uid))
           user = Custom_User.objects.get(id=id)
           if not PasswordResetTokenGenerator().check_token(user, token):
               raise ValidationError('Token is not valid or expired')

           user.set_password(password)
           user.save()
           return attrs

       except DjangoUnicodeDecodeError as identifier:
           PasswordResetTokenGenerator().check_token(user, token)
           raise ValidationError('Token is not valid')
