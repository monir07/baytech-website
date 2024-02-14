from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(required=True, max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2', 'phone_number', "profile_pic")

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # print(self.context['request'].user, "user------------------")
        validated_data.pop("password2")
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class SignInSerializer(Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RefreshTokenSerializer(Serializer):
    refresh = serializers.CharField(required=True)


class ChangePasswordSerializer(Serializer):
    old_password = serializers.CharField(required=True, write_only=True,)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True,)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Two Password fields didn't match."})
        return attrs


class ResetPasswordRequestSerializer(Serializer):
    email = serializers.EmailField(required=True)
    domain = serializers.CharField(required=False)


class AccountActiveSerializer(Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)


class ResetPasswordAcceptSerializer(Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True,)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Two Password fields didn't match."})
        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']

class UserLiteSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'password', 'last_name', 'username', 'email', 'phone', 'address', 'is_active', 'gender','profile_pic_url', 'verified', 'is_staff', 'is_superuser', 'type')