from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
