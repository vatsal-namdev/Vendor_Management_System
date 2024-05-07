from django.test import TestCase, Client
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from .models import Vendor, PurchaseOrder

# Create your tests here.

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="1234567890", address="Test Address", vendor_code="TEST123")

    def test_vendor_list_create_api(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        print("vendor_list", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_detail_api(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        print("vendor_detail", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        data = {'name': 'New Vendor Name', 'contact_details': '4644422168', 'address': 'New Address', 'vendor_code': 'TEST123'}
        response = self.client.put(url, data, content_type='application/json')
        print("update_vendor", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Vendor Name')

    def test_delete_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PurchaseOrderAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="1234567890", address="Test Address", vendor_code="TEST123")
        self.po = PurchaseOrder.objects.create(
            po_number="PO123", 
            vendor=self.vendor, 
            order_date=timezone.now(),  
            delivery_date=timezone.now(),
            items=["Item 1", "Item 2"],
            quantity=10,
            status='pending'
        )

    def test_purchase_order_list_create_api(self):
        url = reverse('purchase-order-list-create')
        response = self.client.get(url)
        print("PO_list", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_purchase_order_detail_api(self):
        url = reverse('purchase-order-detail', kwargs={'pk': self.po.pk})
        response = self.client.get(url)
        print("PO_details", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        url = reverse('purchase-order-detail', kwargs={'pk': self.po.pk})
        data = {
            'po_number': 'PO123',
            'vendor': self.vendor.pk,
            'quantity': 20,
            'items' : ["Item 1", "Item 2"],
            'status': 'completed'
            # Add other fields you want to update here
        }
        response = self.client.put(url, data, content_type='application/json')
        print("PO_update", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        url = reverse('purchase-order-detail', kwargs={'pk': self.po.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        

    def test_acknowledge_purchase_order_api(self):
        url = reverse('purchase-order-acknowledge', kwargs={'pk': self.po.pk})
        response = self.client.post(url)
        print("PO_ack", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)






