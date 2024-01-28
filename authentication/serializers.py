from rest_framework import serializers, exceptions
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'usergroup', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise exceptions.ValidationError('please input password to proceed!')
        
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        instance.username = validated_data['name'].split()[0] + '-' + str(instance.id)
        instance.save()
        return instance
    