from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.utils import timezone
from datetime import timedelta

# Create your views here.


class VendorListCreateAPIView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    def get(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response(status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class PurchaseOrderListCreateAPIView(APIView):
    def get(self, request):
        pos = PurchaseOrder.objects.all()
        vendor_filter = request.query_params.get("vendor", None)
        if vendor_filter:
            pos = pos.filter(vendor=vendor_filter)
        serializer = PurchaseOrderSerializer(pos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return None

    def get(self, request, pk):
        po = self.get_object(pk)
        if not po:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(po)
        return Response(serializer.data)

    def put(self, request, pk):
        po = self.get_object(pk)
        if not po:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(po, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # self.update_vendor_performance(po)  # Trigger performance recalculation
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        po = self.get_object(pk)
        if not po:
            return Response(status=status.HTTP_404_NOT_FOUND)
        po.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    lookup_field = 'pk'

class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the purchase order object
        if not instance:
            return Response({'detail': 'Purchase order not found.'}, status=status.HTTP_404_NOT_FOUND)

        instance.acknowledgment_date = timezone.now()
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
