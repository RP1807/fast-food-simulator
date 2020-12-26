from rest_framework import serializers


class SimConfigSerializer(serializers.Serializer):
    customer_arrival_interval = serializers.IntegerField(required=True)
    order_preparation_time = serializers.IntegerField(required=True)
    order_taker_interval = serializers.IntegerField(required=True)
    time_taken_by_server = serializers.IntegerField(required=True)
    stop_after = serializers.IntegerField(required=True)
