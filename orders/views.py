from django.shortcuts import render
from users.models import User
from rest_framework.generics import (
    ListAPIView, 
    ListCreateAPIView,
    RetrieveAPIView, 
    CreateAPIView, 
    UpdateAPIView, 
    DestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from orders.models import (
    Order, 
    OrderImage, 
    Place, 
    OrderHistory
)
from orders.serializers import (
    OrderSerializer,
    OrderImageSerializer,
    PlaceSerializer,    
)

# Create your views here.


class PlaceListCreateAPIView(ListCreateAPIView):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    permission_classes = (IsAuthenticated, )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PlaceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    permission_classes = (IsAuthenticated, )
    def retrieve(self, request, pk=None):
        queryset = self.queryset
        place = queryset.get(pk=pk)
        serializer = self.serializer_class(place)
        return Response(serializer.data)

    def patch(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.queryset
        place = queryset.get(pk=pk)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None, *args, **kwargs):
        data = request.data
        print(f"Data {data}, type: {type(data)}")
        user: User = User.objects.get(pk=data['user'])
        context: dict = {
            'id': data['id'],
            'user_full_name': user.full_name,
            'user_phone': user.phone,
            'from_place':  data['from_place'],
            'to_place': data['to_place'],
            'price': data['price'],
            'car': data['car'],
            'date': data['date'],
            'description': data['description'],
        }
        print(f"Context: {context}")
        serializer = OrderImageSerializer(data=request.data, many=True)
        if serializer.is_valid():
            qs = serializer.save()
            message = {'detail': qs, 'status': {'code': 200, 'message': 'success', 'simple': status.HTTP_201_CREATED, }}
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            data = {'detail': serializer.errors, 'status': {'code': 400, 'message': 'error', 'simple': status.HTTP_400_BAD_REQUEST}}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class OrderListAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset

    def get(self, request, format=None, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        try:

            data: dict = serializer.data[0]
            print(f"Data {data}")
            
            
            from_place = data.get('from_place')
            # to_place = data.get('to_place')[0]
            print(f"From place {from_place['region']}")
            # print(f"To place {to_place}")
            # print(f"Price {data.get('price')}")
            user = User.objects.get(pk=data['user'])
            context: dict = {
                'id': data['id'],
                'user_full_name': user.full_name,
                'user_phone': user.phone,
                'from_place':  data['from_place'],
                'to_place': data['to_place'],
                'price': data['price'],
                'car': data['car'],
                'date': data['date'],
                'description': data['description'],
            }
            print(f"Context: {context}")
            # print(f"FroM: {from_place}")
            # print(f"To: {to_place}")
        except Exception as e:
            print(f"Error: {e}")
            pass
        return Response(context, status=status.HTTP_200_OK)


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        order = queryset.get(pk=pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def patch(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.queryset
        order = queryset.get(pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderHistoryListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.kwargs['pk'])
        return queryset
    
