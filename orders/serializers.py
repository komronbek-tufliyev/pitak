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
        # print(validated_data)
        user = validated_data['user']
        from_place = validated_data['from_place']
        to_place = validated_data['to_place']
        # from_region = validated_data['from_region']
        # from_city = validated_data['from_city']
        # to_region = validated_data['to_region']
        # to_city = validated_data['to_city']
        car = validated_data['car']
        price = validated_data['price']
        description = validated_data['description']
        is_active = True if validated_data['is_active'] else False
        image = validated_data.pop('image')
        image_list = []
        for img in image:
            context = {
                'user': user,
                'from_place': from_place,
                'to_place': to_place,
                'car': car,
                'price': price,
                'description': description,
                'is_active': is_active,
                'image': img

            }
            photo = Order.objects.create(user=user, from_place=from_place, to_place=to_place, image=img, price=price, is_active=is_active, car=car, description=description)
            image_url = photo.image.url
            image_list.append(image_url)
        return image_list
        


class OrderSerializer(serializers.ModelSerializer):
    # images_set = OrderImageSerializer(many=True)
    from_place = PlaceSerializer()
    to_place = PlaceSerializer()

    class Meta:
        ordering = ['-id']
        model = Order
        fields = '__all__'

    

    def get(self, request, pk=None):
        queryset = self.queryset
        order = queryset.get(pk=pk)
        serializer = self.serializer_class(order)
        


