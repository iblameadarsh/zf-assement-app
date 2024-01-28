from rest_framework import serializers
from authentication.models import User
from zfundsapp.models import Products, Order

class AdvisorAddClientSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'advisor']
        # extra_kwargs = {
        #     'advisor': {'read_only': True}
        # }
    
#     def create(self, validated_data):
#         import ipdb
#         ipdb.set_trace()
#         instance = self.Meta.model(**validated_data)
#         instance.set_password('psf@123')
#         instance.save()
#         instance.username = validated_data['name'].split()[0] + '-' + str(instance.id)
#         instance.save()
#         return instance
    

class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = Order 
        fields = '__all__'

