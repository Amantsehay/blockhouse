# core/utils/serializer.py

from rest_framework import serializers

class EMAStrategySerializer(serializers.Serializer):
    short_window = serializers.IntegerField()
    long_window = serializers.IntegerField()
    stock_symbol = serializers.CharField(max_length=10)
    initial_investment = serializers.DecimalField(max_digits=12, decimal_places=2)


class FetchStockDataSerializer(serializers.Serializer):
    stock_symbol = serializers.CharField(max_length=10)


class PredictStockPriceSerializer(serializers.Serializer):
    stock_symbol = serializers.CharField(max_length=10)
    # model_path = serializers.CharField(max_length=255)  # New field for model path
