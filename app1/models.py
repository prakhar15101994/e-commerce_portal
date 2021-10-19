from django.db import models
from django.contrib.auth.models import User


# Create your models here.

STATE_CHOICES = (
   ("AN","Andaman and Nicobar Islands"),
   ("AP","Andhra Pradesh"),
   ("AR","Arunachal Pradesh"),
   ("AS","Assam"),
   ("BR","Bihar"),
   ("CG","Chhattisgarh"),
   ("CH","Chandigarh"),
   ("DN","Dadra and Nagar Haveli"),
   ("DD","Daman and Diu"),
   ("DL","Delhi"),
   ("GA","Goa"),
   ("GJ","Gujarat"),
   ("HR","Haryana"),
   ("HP","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("MH","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)
 
class Customer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES=(
    ('TW', 'TopWear'),
    ('BW', 'BottomWear'),
    ('M', 'Mobile'),
    ('laptop', 'Laptop'),

)

class Product(models.Model):
    title=models.CharField(max_length=50)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=50)
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    product_image=models.ImageField(upload_to='productimg')
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
            return str(self.id)


STATUS_CHOICES=(
    ('Accepted', 'Accepted'), ('Packed', 'Packed'),('On the way', 'On the way'),('Deliverd', 'Deliverd'),('Cancel', 'Cancel')
)
class OrderPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(auto_created= True)
    status=models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')


# is propert ka num orders.html me total cost ko dekhane k liye use karnge
    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price
