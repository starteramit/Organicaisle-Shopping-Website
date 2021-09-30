from django.db import models
import uuid
from jsonfield import JSONField
# Create your models here.


#START STAPLES PRODUCT
class Add_Staples_Category(models.Model):
    product_category=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="Add Staples Categories"
    def __str__(self):
        return self.product_category
class Add_Staples_Product_Type(models.Model):
    product_category=models.ForeignKey(Add_Staples_Category,default=1,on_delete=models.CASCADE)
    category_type = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="Add Staples Product Types"
    def __str__(self):
        return self.category_type

class offer(models.Model):
    offer=models.CharField(max_length=50)
    def __str__(self):
        return self.offer

class Staples_Product(models.Model):
    product_category = models.ForeignKey(Add_Staples_Category,default=1, on_delete=models.CASCADE)
    category_Type = models.ForeignKey(Add_Staples_Product_Type,default=1, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_quantity=models.CharField(max_length=100)
    product_actual_price=models.IntegerField()
    product_discount_price=models.IntegerField()
    product_image=models.ImageField()
    product_offer = models.ForeignKey(offer, default=1, on_delete=models.SET_DEFAULT)
    product_fullname=models.CharField(max_length=100)


#END STAPLES PRODUCT

#Start Snacks_Beverages
class Add_Snacks_Beverages_Category(models.Model):
    product_category=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="Add Snacks_Beverages Categories"
    def __str__(self):
        return self.product_category
class Add_Snacks_Beverages_Product_Type(models.Model):
    product_category=models.ForeignKey(Add_Snacks_Beverages_Category,default=1,on_delete=models.CASCADE)
    category_type = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="Add Snacks_Beverages Product Types"
    def __str__(self):
        return self.category_type


class Snacks_Beverages_Product_Add(models.Model):
    product_category = models.ForeignKey(Add_Snacks_Beverages_Category,default=1, on_delete=models.CASCADE)
    category_Type = models.ForeignKey(Add_Snacks_Beverages_Product_Type,default=1, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_quantity=models.CharField(max_length=100)
    product_actual_price=models.IntegerField()
    product_discount_price=models.IntegerField()
    product_image=models.ImageField()
    product_offer = models.ForeignKey(offer, default=1, on_delete=models.SET_DEFAULT)
    product_fullname=models.CharField(max_length=100)

#End Snacks_Beverages


#Start Packaged Food
class Add_Packaged_Food_Category(models.Model):
    product_category=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="Add Packaged_Food Categories"
    def __str__(self):
        return self.product_category
class Add_Packaged_Food_Product_Type(models.Model):
    product_category=models.ForeignKey(Add_Packaged_Food_Category,default=1,on_delete=models.CASCADE)
    category_type = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="Add Packaged_Food Product Types"
    def __str__(self):
        return self.category_type


class Packaged_Food_Product_Add(models.Model):
    product_category = models.ForeignKey(Add_Packaged_Food_Category,default=1, on_delete=models.CASCADE)
    category_Type = models.ForeignKey(Add_Packaged_Food_Product_Type,default=1, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_quantity=models.CharField(max_length=100)
    product_actual_price=models.IntegerField()
    product_discount_price=models.IntegerField()
    product_image=models.ImageField()
    product_offer = models.ForeignKey(offer, default=1, on_delete=models.SET_DEFAULT)
    product_fullname=models.CharField(max_length=100)

#End Packaged Food

#Start Personal And baby CAre
class Add_Personal_Baby_care_Category(models.Model):
    product_category=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="Add Personal_Baby_care Categories"
    def __str__(self):
        return self.product_category
class Add_Personal_Baby_care_Product_Type(models.Model):
    product_category=models.ForeignKey(Add_Personal_Baby_care_Category,default=1,on_delete=models.CASCADE)
    category_type = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="Add Personal_Baby_care Product Types"
    def __str__(self):
        return self.category_type


class Personal_Baby_care_Product_Add(models.Model):
    product_category = models.ForeignKey(Add_Personal_Baby_care_Category,default=1, on_delete=models.CASCADE)
    category_Type = models.ForeignKey(Add_Personal_Baby_care_Product_Type,default=1, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_quantity=models.CharField(max_length=100)
    product_actual_price=models.IntegerField()
    product_discount_price=models.IntegerField()
    product_image=models.ImageField()
    product_offer = models.ForeignKey(offer, default=1, on_delete=models.SET_DEFAULT)
    product_fullname=models.CharField(max_length=100)

#End Personal and Baby Care



#Start Household_care
class Add_Household_care_Category(models.Model):
    product_category=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="Add Household_care Categories"
    def __str__(self):
        return self.product_category
class Add_Household_care_Product_Type(models.Model):
    product_category=models.ForeignKey(Add_Household_care_Category,default=1,on_delete=models.CASCADE)
    category_type = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="Add Household_care Product Types"
    def __str__(self):
        return self.category_type


class Household_care_Product_Add(models.Model):
    product_category = models.ForeignKey(Add_Household_care_Category,default=1, on_delete=models.CASCADE)
    category_Type = models.ForeignKey(Add_Household_care_Product_Type,default=1, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_quantity=models.CharField(max_length=100)
    product_actual_price=models.IntegerField()
    product_discount_price=models.IntegerField()
    product_image=models.ImageField()
    product_offer = models.ForeignKey(offer, default=1, on_delete=models.SET_DEFAULT)
    product_fullname=models.CharField(max_length=100)
#End Household_care



#Start Dairy
class Add_Dairy_Category(models.Model):
    product_category=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="Add Dairy Categories"
    def __str__(self):
        return self.product_category
class Add_Dairy_Product_Type(models.Model):
    product_category=models.ForeignKey(Add_Dairy_Category,default=1,on_delete=models.CASCADE)
    category_type = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="Add Dairy Product Types"
    def __str__(self):
        return self.category_type


class Dairy_Product_Add(models.Model):
    product_category = models.ForeignKey(Add_Dairy_Category,default=1, on_delete=models.CASCADE)
    category_Type = models.ForeignKey(Add_Dairy_Product_Type,default=1, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    product_quantity=models.CharField(max_length=100)
    product_actual_price=models.IntegerField()
    product_discount_price=models.IntegerField()
    product_image=models.ImageField()
    product_offer = models.ForeignKey(offer, default=1, on_delete=models.SET_DEFAULT)
    product_fullname=models.CharField(max_length=100)
#End Dairy

#start Deal Of The Weak

class Deal_of_The_Weak(models.Model):
    product_name = models.CharField(max_length=100)
    product_quantity = models.CharField(max_length=100)
    product_actual_price = models.IntegerField()
    product_discount_price = models.IntegerField()
    product_image = models.ImageField()
    product_offer = models.ForeignKey(offer, default=1, on_delete=models.SET_DEFAULT)
    product_fullname = models.CharField(max_length=100)



#Start Special Offer
class Special_offer(models.Model):
    product_name = models.CharField(max_length=100)
    product_quantity = models.CharField(max_length=100)
    product_actual_price = models.IntegerField()
    product_discount_price = models.IntegerField()
    product_image = models.ImageField()
    product_offer = models.ForeignKey(offer, default=1, on_delete=models.SET_DEFAULT)
    product_fullname = models.CharField(max_length=100)


# Start Slider

class Slider(models.Model):
    slider_img=models.ImageField()

class Order_Status(models.Model):
    order_status = models.CharField(max_length=100)
    def __str__(self):
        return self.order_status
#Cart table start
class Cart(models.Model):
    username=models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_weight = models.CharField(max_length=100)
    product_price = models.CharField(max_length=100)
    product_quantity = models.CharField(max_length=20)
    total_price = models.CharField(max_length=100)
    order_status = models.BooleanField(default=False)





class Shipping_Address(models.Model):
    username = models.CharField(max_length=100)
    # product_detail = JSONField()
    product_details = JSONField()
    total_price = models.CharField(max_length=100)
    full_name=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    full_address=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    date_time=models.DateField(auto_now_add=True, blank=True)
    delevery_date_time=models.DateField(null=True)
    order_id = models.UUIDField(max_length=8,default = uuid.uuid4,editable = False) # want to generate new unique id from this field
    order_status = models.ForeignKey(Order_Status,default=1,on_delete=models.CASCADE)
    no_of_items = models.CharField(max_length=100)
    def __str__(self):
        return self.username









