from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)

    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    def clean(self):
        if Vendor.objects.filter(vendor_code=self.vendor_code).exists():
            raise ValidationError("Vendor with this vendor code already exists.")
        return super().clean()
    
    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        if total_completed_pos == 0:
            return 0.0
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        return on_time_delivered_pos.count() / total_completed_pos

    def calculate_quality_rating_average(self):
        completed_pos_with_quality_rating = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        if completed_pos_with_quality_rating.exists():
            return completed_pos_with_quality_rating.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
        return 0.0

    def calculate_average_response_time(self):
        completed_pos_with_acknowledgment = self.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
        if completed_pos_with_acknowledgment.exists():
            response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos_with_acknowledgment]
            return sum(response_times) / len(response_times)
        return 0.0

    def calculate_fulfilment_rate(self):
        total_pos = self.purchaseorder_set.count()
        if total_pos == 0:
            return 0.0
        successful_pos = self.purchaseorder_set.filter(status='completed')
        return successful_pos.count() / total_pos
    
    def update_performance_metrics(self):
        on_time_delivery_rate = self.calculate_on_time_delivery_rate()
        quality_rating_avg = self.calculate_quality_rating_average()
        average_response_time = self.calculate_average_response_time()
        fulfillment_rate = self.calculate_fulfilment_rate()

        # Update performance metrics of the vendor
        self.on_time_delivery_rate = on_time_delivery_rate
        self.quality_rating_avg = quality_rating_avg
        self.average_response_time = average_response_time
        self.fulfillment_rate = fulfillment_rate
        self.save()

    

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(blank=True, null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"
    
    def save(self, *args, **kwargs):
        # Call the parent class's save method
        super().save(*args, **kwargs)

        # Check if the status is changed to "completed"
        if self.status == 'completed':
            # Calculate performance metrics
            on_time_delivery_rate = self.vendor.calculate_on_time_delivery_rate()
            quality_rating_avg = self.vendor.calculate_quality_rating_average()
            average_response_time = self.vendor.calculate_average_response_time()
            fulfillment_rate = self.vendor.calculate_fulfilment_rate()  # corrected method name

            # Create a new HistoricalPerformance record
            HistoricalPerformance.objects.create(
                vendor=self.vendor,
                date=self.delivery_date,  # or any date you want to associate with this record
                on_time_delivery_rate=on_time_delivery_rate,
                quality_rating_avg=quality_rating_avg,
                average_response_time=average_response_time,
                fulfillment_rate=fulfillment_rate
            )
    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
