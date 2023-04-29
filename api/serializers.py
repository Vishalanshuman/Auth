from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER
import re
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email','mobile', 'password']

    def create(self, validated_data):
        user  = User.objects.create_user(**validated_data)
        send_mail(
            "Account Created Successfully",
            f'''
            Thanks for register on our Website.
            Your username is --{validated_data['username']} and your password is --{validated_data['password']}
            ''',
            EMAIL_HOST_USER,
            [validated_data['email']],
            fail_silently=False,
        )
        user.set_password(validated_data['password'])
        return user
    
    def validate(self, attrs):
        try:
            num = int(attrs['mobile'])
        except:
            raise serializers.ValidationError('Mobile number must be an integer.')
        SpecialSym=['$','@','#']
        if len(attrs['password']) < 8:
            raise serializers.ValidationError("Make sure your password is at lest 8 letters")
        elif re.search('[0-9]',attrs['password']) is None:
            raise serializers.ValidationError("Password should contains Capital letter, alphnumeric and some special character")
        elif re.search('[A-Z]',attrs['password']) is None: 
            raise serializers.ValidationError("Password should contains Capital letter, alphnumeric and some special character")
        elif not any(char in SpecialSym for char in attrs['password']):
            raise serializers.ValidationError('Password should contains a Capital letter, alphnumeric and some special character')
        else:
            return attrs

        
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200)
    class Meta:
        model = User
        fields = ['username', 'password']
