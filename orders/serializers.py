from orders.models import Order, Place, OrderImage, OrderHistory
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class OrderImageSerializer(serializers.ModelSerializer):
    image = serializers.ListField(
        child=serializers.FileField(
            max_length=100000,
            allow_empty_file=False,
            use_url=True,   
        )
    )
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        fin = open('output.txt', 'w')
        fin.write(str(validated_data))
        
        # print(validated_data)
        user = validated_data['user']
        from_place = validated_data['from_place']
        to_place = validated_data['to_place']
        price = validated_data['price']
        is_active = True if validated_data['is_active'] else False
        image = validated_data.pop('image')
        image_list = []
        fin.write(str(validated_data))
        for img in image:
            photo = Order.objects.create(user=user, from_place=from_place, to_place=to_place, image=img, price=price, is_active=is_active)
            image_url = photo.image.url
            image_list.append(image_url)
        return image_list
        


class OrderSerializer(serializers.ModelSerializer):
    # images_set = OrderImageSerializer(many=True)
    class Meta:
        ordering = ['-id']
        model = Order
        fields = '__all__'


