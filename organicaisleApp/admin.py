from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *



class itemfilter(admin.ModelAdmin):
    list_display = ('id','product_name')
    list_filter = ('product_fullname','product_category' ,'category_Type')
    search_fields = ('product_fullname', 'product_name')
# Register your models here.
class staples_product_display(admin.ModelAdmin):
    list_display = ('id','product_name')
    list_filter = ('product_name',)
class staples_product_type_display(admin.ModelAdmin):
    list_display = ('id','category_type','product_category_id')

admin.site.register(Staples_Product,itemfilter)
#admin.site.register(Add_Staples_Category)
#admin.site.register(Add_Staples_Product_Type,staples_product_type_display)
admin.site.register(offer)

admin.site.register(Snacks_Beverages_Product_Add,itemfilter)
#admin.site.register(Add_Snacks_Beverages_Category)
#admin.site.register(Add_Snacks_Beverages_Product_Type)


admin.site.register(Packaged_Food_Product_Add,itemfilter)
#admin.site.register(Add_Packaged_Food_Category)
#admin.site.register(Add_Packaged_Food_Product_Type)


admin.site.register(Personal_Baby_care_Product_Add,itemfilter)
#admin.site.register(Add_Personal_Baby_care_Category)
#admin.site.register(Add_Personal_Baby_care_Product_Type)

admin.site.register(Household_care_Product_Add,itemfilter)
#admin.site.register(Add_Household_care_Category)
#admin.site.register(Add_Household_care_Product_Type)

admin.site.register(Dairy_Product_Add,itemfilter)
#admin.site.register(Add_Dairy_Category)
#admin.site.register(Add_Dairy_Product_Type)

admin.site.register(Deal_of_The_Weak)

admin.site.register(Special_offer)

admin.site.register(Slider)



#shipping address
class Shipping_Address_admin(admin.ModelAdmin):
    list_display = ('id','order_id','username','product_details','total_price','payment_method','delevery_date_time','order_status','full_name','mobile','email','full_address','landmark','city','pincode','date_time')
    search_fields = ('username', 'delevery_date_time','date_time','order_id','payment_method','full_name','mobile','email','full_address',)
admin.site.register(Shipping_Address,Shipping_Address_admin)
admin.site.register(Order_Status)


