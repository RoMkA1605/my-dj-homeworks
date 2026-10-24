from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
       positions_data = self.initial_data.get('positions', [])
       stock = Stock.objects.create(**validated_data)

       for position in positions_data:
            StockProduct.objects.create(
                stock=stock,
                product_id=position['product'],
                quantity=position.get('quantity', 1),
                price=position['price']
            )
            return stock

    def update(self, instance, validated_data):
       positions_data = self.initial_data.get('positions', [])

       instance.address = validated_data.get('address', instance.address)
       instance.save()

       for position in positions_data:
            StockProduct.objects.update_or_create(
                stock=instance,
                product_id=position['product'],
                defaults={
                    'quantity': position.get('quantity', 1),
                    'price': position['price']
                }
            )
            return instance