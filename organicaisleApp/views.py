from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q
from paytm import Checksum
from django.contrib import messages
from array import *
from django.views.decorators.csrf import csrf_exempt
import uuid

from django.contrib.auth import authenticate,login,logout
# Create your views here.

MERCHANT_KEY = '7@p3UOxG5s23JnfI'

def index(request):
    username = request.user
    deal_of_weak=Deal_of_The_Weak.objects.all()
    special_offer=Special_offer.objects.all()
    slider_image=Slider.objects.all()
    Shipping_Address.objects.filter(username=username,payment_method="Online Payment").delete()
    product_data = Cart.objects.filter(username=username, order_status=False)
    no_of_item = 0
    for i in product_data:
        no_of_item +=1
    context={'deal_of_weak':deal_of_weak,'special_offer':special_offer,'slider_image':slider_image,'no_of_item':no_of_item}
    return render(request,'index.html',context)

def search(request):
    username = request.user
    query=request.GET.get('search')
    staples_product=Staples_Product.objects.filter(Q(product_name__icontains=query) | Q(product_fullname__icontains=query))
    Snacks_Beverages_Product = Snacks_Beverages_Product_Add.objects.filter(Q(product_name__icontains=query) | Q(product_fullname__icontains=query))
    Packaged_Food_Product=Packaged_Food_Product_Add.objects.filter(Q(product_name__icontains=query) | Q(product_fullname__icontains=query))
    Personal_Baby_care_Product=Personal_Baby_care_Product_Add.objects.filter(Q(product_name__icontains=query) | Q(product_fullname__icontains=query))
    Household_care_Product=Household_care_Product_Add.objects.filter(Q(product_name__icontains=query) | Q(product_fullname__icontains=query))
    Dairy_Product=Dairy_Product_Add.objects.filter(Q(product_name__icontains=query) | Q(product_fullname__icontains=query))
    product_data = Cart.objects.filter(username=username, order_status=False)
    no_of_item = 0
    for i in product_data:
        no_of_item += 1
    if staples_product:
        search_product=staples_product
        return render(request,'search.html',{'search_product':search_product,'no_of_item':no_of_item})
    elif Snacks_Beverages_Product:
        search_product =Snacks_Beverages_Product
        return render(request, 'search.html', {'search_product': search_product,'no_of_item':no_of_item})
    elif Snacks_Beverages_Product:
        search_product =Packaged_Food_Product
        return render(request, 'search.html', {'search_product': search_product,'no_of_item':no_of_item})
    elif Snacks_Beverages_Product:
        search_product =Personal_Baby_care_Product
        return render(request, 'search.html', {'search_product': search_product,'no_of_item':no_of_item})
    elif Snacks_Beverages_Product:
        search_product =Household_care_Product
        return render(request, 'search.html', {'search_product': search_product,'no_of_item':no_of_item})
    elif Snacks_Beverages_Product:
        search_product =Dairy_Product
        return render(request, 'search.html', {'search_product': search_product,'no_of_item':no_of_item})
    else:
        search_product=False
        return render(request, 'search.html', {'search_product': search_product,'no_of_item':no_of_item})






def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"Username Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,"Email Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                email=email,
                                                password=password1)
                user.save()
                return render(request,'login.html')
        else:
            messages.warning(request, "Password Not Match")
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        pro_name = request.POST['pro_name']
        price = request.POST['price']
        pro_quantity = request.POST['pro_quantity']

        if user is not None:
            auth.login(request,user)
            return render(request,'cart.html',{'pro_name':pro_name,'pro_quantity':pro_quantity,'price':price})

        else:
            messages.error(request,'Invalid Credential Please Try Again')
            return redirect('login')
    else:
        buynow = request.GET.get('buynow')
        pro_name = request.GET['pro_name']
        price = request.GET['price']
        pro_quantity = request.GET['pro_quantity']
        return render(request,'login.html',{'buynow':buynow,'pro_name':pro_name,'pro_quantity':pro_quantity,'price':price})
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Invalid Credential Please Try Again')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def cart(request):
    username = request.user
    product_data = Cart.objects.filter(username=username,order_status=False)
    no_of_item = 0
    for i in product_data:
        no_of_item += 1
    total = 0
    delivery = 40
    # unique_id = []
    for i in product_data:
        total = total + int(i.total_price)
        # unique_id.append(i.unique_id)

    total = total + delivery
    return render(request,'cart.html',{'product_data':product_data,'total':total,'no_of_item':no_of_item})


def addtocart(request):

        username = request.user
        product_name = request.GET['pro_name']
        pro_weight=request.GET['pro_weight']
        price=request.GET['price']
        product_quantity=request.GET['pro_quantity']
        # unique_id=request.GET['unique_id']
        total_price = int(price) * int(product_quantity)
        obj = Cart()
        obj.username = username
        obj.product_name = product_name
        obj.product_weight = pro_weight
        obj.product_price = price
        obj.product_quantity = product_quantity
        obj.total_price =total_price
        # obj.unique_id = unique_id
        obj.save()
        return redirect('/cart/')

def remove(request):
    product_id=request.GET['pro_remove']
    Cart.objects.filter(id=product_id).delete()
    return redirect('/cart/')


def shipping_address(request):
    if request.method == 'POST':
        username = request.user
        product_data = Cart.objects.filter(username=username, order_status=False)
        total = 0
        delivery = 40
        # product_detail = {}
        product_details = {}
        no_of_item=0
        for i in product_data:
            total = total + int(i.total_price)
        z=0
        for j in product_data:
            # product_detail[z] = {'unique_id': j.unique_id, 'product_quantity': j.product_quantity,
            #                      'sub_total_price': j.total_price}
            product_details[z] = {'product_name': j.product_name, 'product_weight': j.product_weight,
                                  'product_price': j.product_price, 'product_quantity': j.product_quantity,
                                  'total_price': j.total_price}
            z+=1
            no_of_item += 1

        total = total + delivery
        full_name=request.POST['full_name']
        mobile=request.POST['mobile']
        email=request.POST['email']
        full_address=request.POST['full_address']
        landmark=request.POST['landmark']
        city=request.POST['city']
        pincode=request.POST['pincode']
        payment=request.POST['payment']

        if payment=="Cash On Delivery":
            obj = Shipping_Address()
            obj.username = username
            # obj.product_detail = product_detail
            obj.total_price = total
            obj.full_name = full_name
            obj.mobile= mobile
            obj.email = email
            obj.full_address = full_address
            obj.landmark = landmark
            obj.city= city
            obj.pincode = pincode
            obj.payment_method = payment
            obj.product_details=product_details
            obj.no_of_items=no_of_item
            obj.save()
            unique_id = []
            for l in product_data:
                # unique_id.append(l.unique_id)
                Cart.objects.filter(username=username, order_status=False).update(order_status=True)
            # for un in unique_id:
                # Cart.objects.filter(username=username,order_status=False).update(order_status=True)
            messages.success(request, 'Order Successful')
            return redirect('/', {'no_of_item': no_of_item})
        elif payment == "Online Payment":
            obj = Shipping_Address()
            obj.username = username
            # obj.product_detail = product_detail
            obj.total_price = total
            obj.full_name = full_name
            obj.mobile= mobile
            obj.email = email
            obj.full_address = full_address
            obj.landmark = landmark
            obj.city= city
            obj.pincode = pincode
            obj.payment_method = payment
            obj.product_details=product_details
            obj.no_of_items=no_of_item
            # unique_id = []
            # for l in product_data:
            #     unique_id.append(l.unique_id)
            for un in product_data:
                Cart.objects.filter(username=username,order_status=False).update(order_status=True)
            param_dict={
                'MID': 'LMhiUV46855068961546',
                'ORDER_ID': str(obj.order_id),
                'TXN_AMOUNT': str(total),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            obj.save()
            return render(request,'paytm.html',{'param_dict':param_dict,'order_id':obj.order_id})

    else:
        username = request.user
        pro_name = request.GET['pro_name']
        price = request.GET['price']
        pro_quantity = request.GET['pro_quantity']
        return render(request,'shipping_address.html',{'pro_name':pro_name,'pro_quantity':pro_quantity,'price':price})


#my order start------------------------------------------------------------
def myorder(request):
    username = request.user
    myorder_data_processing=Shipping_Address.objects.filter(Q(username=username,order_status=1) | Q(username=username,order_status=2))
    myorder_data_delivered=Shipping_Address.objects.filter(username=username,order_status=3)
    product_data = Cart.objects.filter(username=username, order_status=False)
    Shipping_Address.objects.filter(username=username,payment_method="Online Payment").delete()
    no_of_item = 0
    for i in product_data:
        no_of_item += 1
    return render(request,'myorder.html',{'myorder_data_processing':myorder_data_processing,'myorder_data_delivered':myorder_data_delivered,'no_of_item':no_of_item})

#Handle Payment------------------------------------------------------------
@csrf_exempt
def handlerequest(request):
    username=request.user
    order_id=request.POST['ORDERID']
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            Shipping_Address.objects.filter(username=username,order_id=order_id).update(payment_method='online payment successful')
            messages.success(request, 'Order Successful')
        else:
            Shipping_Address.objects.filter(username=username,order_id=order_id).delete()
            messages.error(request, 'Order Not Successful.')
            print('order was not successful because' + response_dict['RESPMSG'])
    return redirect('/', {'response': response_dict})


def All_Product(request):
    username = request.user
    product_data = Cart.objects.filter(username=username, order_status=False)
    no_of_item = 0
    for i in product_data:
        no_of_item += 1
    #-----------------------------------------------------------------------------------------------------
    #---------------------------------------Start All Staples Product-------------------------------------
    #-----------------------------------------------------------------------------------------------------
    staples_type=request.POST.get('staples_type')
    #start all dal----------------------------------------------------------------------------
    if staples_type=="Dals_pulses":
        product_type_name="Dals and Pulses"
        pro_data=Staples_Product.objects.filter(product_category_id=1)
        return render(request,'allproduct.html',{'pro_data':pro_data,'product_type_name':product_type_name,'no_of_item':no_of_item})
    #end all dal----------------------------------------------------------------------------
    #start ghee and oil all-----------------------------------------------------------
    if staples_type=="ghee_oils":
        product_type_name="Ghee and Oils"
        pro_data=Staples_Product.objects.filter(product_category_id=2)
        return render(request,'allproduct.html',{'pro_data':pro_data,'product_type_name':product_type_name,'no_of_item':no_of_item})
    #end ghee and oil all-----------------------------------------------------------

     # start all atta----------------------------------------------------------------------------
    if staples_type == "atta_flour":
         product_type_name = "Atta And Flour"
         pro_data = Staples_Product.objects.filter(product_category_id=3)
         return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end all atta----------------------------------------------------------------------------

    # start all masala & Spices----------------------------------------------------------------------------
    if staples_type == "masala_spices":
        product_type_name = "Masala Spices And Salt"
        pro_data = Staples_Product.objects.filter(product_category_id=4)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end all masala & Spices----------------------------------------------------------------------------

    # start all rice products----------------------------------------------------------------------------
    if staples_type == "rice_sugar":
        product_type_name = "Rice Products And Sugar"
        pro_data = Staples_Product.objects.filter(product_category_id=5)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end all rice products----------------------------------------------------------------------------

    # start all rice products----------------------------------------------------------------------------
    if staples_type == "dryfruit_seed":
        product_type_name = "Dry Fruits,Nuts And Seeds"
        pro_data = Staples_Product.objects.filter(product_category_id=6)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
        # end all rice products----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------End All Staples Product-------------------------------------
    # -----------------------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------------------
        # ---------------------------------------Start All Snacks Product-------------------------------------
        # -----------------------------------------------------------------------------------------------------
    snacks_type = request.POST.get('snacks_type')
    # start all biscuits ----------------------------------------------------------------------------
    if snacks_type == "biscuits":
        product_type_name = "Biscuits"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end all biscuits----------------------------------------------------------------------------
    # start Chips_Namkeen_Snacks all-----------------------------------------------------------
    if snacks_type == "Chips_Namkeen_Snacks":
        product_type_name = "Chips,Namkeen & Snacks"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end Chips_Namkeen_Snacks all-----------------------------------------------------------
     # start Chips_Namkeen_Snacks all-----------------------------------------------------------
    if snacks_type == "tea_coffee":
        product_type_name = "Tea & Coffee"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end Chips_Namkeen_Snacks all-----------------------------------------------------------
    # start Chips_Namkeen_Snacks all-----------------------------------------------------------
    if snacks_type == "juices":
        product_type_name = "Juices"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end Chips_Namkeen_Snacks all-----------------------------------------------------------
        # start Chips_Namkeen_Snacks all-----------------------------------------------------------
    if snacks_type == "health_drink":
        product_type_name = "Soft & Health Drinks"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
        # end Chips_Namkeen_Snacks all-----------------------------------------------------------


    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------End All Snacks and beverages Product--------------------------
    # -----------------------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------------------
        # ---------------------------------------Start All Packaged Food Product-------------------------------------
        # -----------------------------------------------------------------------------------------------------
    packaged_type = request.POST.get('packaged_type')
    # start all Breakfast Cereals ----------------------------------------------------------------------------
    if packaged_type == "breakfast":
        product_type_name = "Breakfast Cereals"
        pro_data = Packaged_Food_Product_Add.objects.filter(product_category_id=1)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end all Breakfast Cereals----------------------------------------------------------------------------
    # start noodles_pasta all-----------------------------------------------------------
    if packaged_type == "noodles_pasta":
        product_type_name = "Noodles & Pasta"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end noodles_pasta all-----------------------------------------------------------
     # start ketchup_spread all-----------------------------------------------------------
    if packaged_type == "ketchup_spread":
        product_type_name = "Ketchups & Spreads"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end ketchup_spread all-----------------------------------------------------------
    # start choclate_sweet all-----------------------------------------------------------
    if packaged_type == "choclate_sweet":
        product_type_name = "Chocolates & Sweets"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # end choclate_sweet all-----------------------------------------------------------
        # start jams_honey all-----------------------------------------------------------
    if packaged_type == "jams_honey":
        product_type_name = "Jams & Honey"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
        # end jams_honey all-----------------------------------------------------------
        # start pickle_chutney all-----------------------------------------------------------
    if packaged_type == "pickle_chutney":
        product_type_name = "Pickles & Chutney"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=6)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
        # end pickle_chutney all-----------------------------------------------------------
    # start ready_cook all-----------------------------------------------------------
    if packaged_type == "ready_cook":
        product_type_name = "Ready To Cook"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=7)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
        # end ready_cook all-----------------------------------------------------------
    # start cooking_sauce all-----------------------------------------------------------
    if packaged_type == "cooking_sauce":
        product_type_name = "Cooking Sauces & Vineger"
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=8)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
        # end cooking_sauce all-----------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------End All Packaged Food Product--------------------------------------
    # -----------------------------------------------------------------------------------------------------


    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------Start All Personal & Baby Care Product--------------------------------------
    # -----------------------------------------------------------------------------------------------------
    care_type = request.POST.get('care_type')
    if care_type == "soaps_body_wash":
        product_type_name = "Soaps & Body Wash"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=1)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "hair_care":
        product_type_name = "Hair Care"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=2)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "oral_care":
        product_type_name = "Oral Care"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=3)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "deos_perfumes":
        product_type_name = "Deos,Perfumes & Talc"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=4)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "creams_lotions":
        product_type_name = "Creams,Lotions & Skin Care"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "diapers_wipes":
        product_type_name = "Diapers & Wipes"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=6)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "kajal_makeup":
        product_type_name = "Kajal & Makeup"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=7)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "welleness":
        product_type_name = "Welleness & Common Pharma"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=8)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "sanitary_needs":
        product_type_name = "Sanitary Needs"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=9)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "shaving":
        product_type_name = "Shaving Needs"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=10)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "baby_bath_skin":
        product_type_name = "Baby Bath & Skin Care"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=11)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if care_type == "baby_food":
        product_type_name = "Baby Foods"
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=12)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})

    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------End All Personal & Baby Care Product--------------------------------------
    # -----------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------Start All Household Care--------------------------------------
    # -----------------------------------------------------------------------------------------------------
    household_type = request.POST.get('household_type')
    if household_type == "detergents_cleaners":
        product_type_name = "Detergents & Utensil Cleaners"
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=1)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if household_type == "shoe_care":
        product_type_name = "Shoe Care"
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=2)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if household_type == "floor_cleaners":
        product_type_name = "Floor & Other Cleaners"
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=3)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if household_type == "pet_food":
        product_type_name = "Pet Food"
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=4)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if household_type == "repellants":
        product_type_name = "Repellants & Freshners"
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=5)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if household_type == "pooja":
        product_type_name = "Pooja Needs"
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=6)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    if household_type == "paper_disposable":
        product_type_name = "Paper & Disposables"
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=7)
        return render(request, 'allproduct.html',{'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------End All Household Care--------------------------------------
    # -----------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------Start All Dairy--------------------------------------
    # -----------------------------------------------------------------------------------------------------
    dairy_type = request.POST.get('dairy_type')
    if dairy_type == "dairy":
        product_type_name = "Dairy"
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        return render(request, 'allproduct.html', {'pro_data': pro_data, 'product_type_name': product_type_name,'no_of_item':no_of_item})
    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------End All Dairy--------------------------------------
    # -----------------------------------------------------------------------------------------------------




    return render(request,'allproduct.html')

def Single_Product(request):
    username = request.user
    product_data = Cart.objects.filter(username=username, order_status=False)
    no_of_item = 0
    for i in product_data:
        no_of_item += 1
    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------Start single staples Product-------------------------------------
    # -----------------------------------------------------------------------------------------------------
    staples_type = request.POST.get('staples_type')
    #start single Dal -------------------------------------------------------------------------
    if staples_type=="Toor":
        product_type_name = "Dals and Pulses"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=2)
        pro_data = Staples_Product.objects.filter(product_category_id=1)
        heading="Toor Dal"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="urad":
        product_type_name = "Dals and Pulses"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=3)
        pro_data = Staples_Product.objects.filter(product_category_id=1)
        heading="Urad Dal"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="moong":
        product_type_name = "Dals and Pulses"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=4)
        pro_data = Staples_Product.objects.filter(product_category_id=1)
        heading="Moong Dal"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="chana":
        product_type_name = "Dals and Pulses"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=5)
        pro_data = Staples_Product.objects.filter(product_category_id=1)
        heading="Chana Dal"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="other":
        product_type_name = "Dals and Pulses"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=6)
        pro_data = Staples_Product.objects.filter(product_category_id=1)
        heading="Other Pulses"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    #end single dal---------------------------------------------------------------------------------

    #start single Ghee And Oil------------------------------------------------------------------------
    if staples_type=="sunflower":
        product_type_name = "Ghee and Oils"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=7)
        pro_data = Staples_Product.objects.filter(product_category_id=2)
        heading="Other Pulses"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="ricebran":
        product_type_name = "Ghee and Oils"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=8)
        pro_data = Staples_Product.objects.filter(product_category_id=2)
        heading="Other Pulses"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="groundnut":
        product_type_name = "Ghee and Oils"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=10)
        pro_data = Staples_Product.objects.filter(product_category_id=2)
        heading="Other Pulses"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="mustard":
        product_type_name = "Ghee and Oils"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=11)
        pro_data = Staples_Product.objects.filter(product_category_id=2)
        heading="Other Pulses"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="otheroil":
        product_type_name = "Ghee and Oils"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=12)
        pro_data = Staples_Product.objects.filter(product_category_id=2)
        heading="Other Pulses"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)
    if staples_type=="ghee":
        product_type_name = "Ghee and Oils"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=13)
        pro_data = Staples_Product.objects.filter(product_category_id=2)
        heading="Other Pulses"
        context={'single_pro_data':single_pro_data,'pro_data':pro_data,'product_type_name':product_type_name,'heading':heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html',context)

    #End single Ghee And Oil------------------------------------------------------------------------

    # start single atta -------------------------------------------------------------------------
    if staples_type == "wheat":
        product_type_name = "Atta And Flour"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=15)
        pro_data = Staples_Product.objects.filter(product_category_id=3)
        heading = "Wheat Flour"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "rice":
        product_type_name = "Atta And Flour"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=16)
        pro_data = Staples_Product.objects.filter(product_category_id=3)
        heading = "Rice Flour"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "maida":
        product_type_name = "Atta And Flour"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=17)
        pro_data = Staples_Product.objects.filter(product_category_id=3)
        heading = "Maida"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "otherflour":
        product_type_name = "Atta And Flour"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=18)
        pro_data = Staples_Product.objects.filter(product_category_id=3)
        heading = "Other Flour"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "grains":
        product_type_name = "Atta And Flour"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=19)
        pro_data = Staples_Product.objects.filter(product_category_id=3)
        heading = "Grains"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "suji":
        product_type_name = "Atta And Flour"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=20)
        pro_data = Staples_Product.objects.filter(product_category_id=3)
        heading = "Rava And Sooji"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "besan":
        product_type_name = "Atta And Flour"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=21)
        pro_data = Staples_Product.objects.filter(product_category_id=3)
        heading = "Besan"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # end single atta---------------------------------------------------------------------------------

    # start single masala spices and salt -------------------------------------------------------------------------
    if staples_type == "whole":
        product_type_name = "Masala Spices And Salt"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=22)
        pro_data = Staples_Product.objects.filter(product_category_id=4)
        heading = "Whole Spices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "powder":
        product_type_name = "Masala Spices And Salt"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=23)
        pro_data = Staples_Product.objects.filter(product_category_id=4)
        heading = "Powdered Spices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "ready":
        product_type_name = "Masala Spices And Salt"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=24)
        pro_data = Staples_Product.objects.filter(product_category_id=4)
        heading = "Ready Spices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "cooking":
        product_type_name = "Masala Spices And Salt"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=25)
        pro_data = Staples_Product.objects.filter(product_category_id=4)
        heading = "Cooking Pastes & Puries"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "herbs":
        product_type_name = "Masala Spices And Salt"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=26)
        pro_data = Staples_Product.objects.filter(product_category_id=4)
        heading = "Herbs & Seasoning"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "salt":
        product_type_name = "Masala Spices And Salt"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=27)
        pro_data = Staples_Product.objects.filter(product_category_id=4)
        heading = "Salt"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # end single masala spices and salt---------------------------------------------------------------------------------

        # start single rice products and sugar -------------------------------------------------------------------------
    if staples_type == "masoori":
         product_type_name = "Rice Products And Sugar"
         single_pro_data = Staples_Product.objects.filter(category_Type_id=28)
         pro_data = Staples_Product.objects.filter(product_category_id=5)
         heading = "Sona Masoori Rice"
         context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                       'heading': heading,'no_of_item':no_of_item}
         return render(request, 'single_product.html', context)
    if staples_type == "otherrice":
         product_type_name = "Rice Products And Sugar"
         single_pro_data = Staples_Product.objects.filter(category_Type_id=29)
         pro_data = Staples_Product.objects.filter(product_category_id=5)
         heading = "Other Rice Variety"
         context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                       'heading': heading,'no_of_item':no_of_item}
         return render(request, 'single_product.html', context)
    if staples_type == "poha":
         product_type_name = "Rice Products And Sugar"
         single_pro_data = Staples_Product.objects.filter(category_Type_id=30)
         pro_data = Staples_Product.objects.filter(product_category_id=5)
         heading = "Poha"
         context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                       'heading': heading,'no_of_item':no_of_item}
         return render(request, 'single_product.html', context)
    if staples_type == "puffed":
         product_type_name = "Rice Products And Sugar"
         single_pro_data = Staples_Product.objects.filter(category_Type_id=31)
         pro_data = Staples_Product.objects.filter(product_category_id=5)
         heading = "Puffed Rice"
         context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                       'heading': heading,'no_of_item':no_of_item}
         return render(request, 'single_product.html', context)
    if staples_type == "basmati":
         product_type_name = "Rice Products And Sugar"
         single_pro_data = Staples_Product.objects.filter(category_Type_id=32)
         pro_data = Staples_Product.objects.filter(product_category_id=5)
         heading = "Basmati Rice"
         context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                       'heading': heading,'no_of_item':no_of_item}
         return render(request, 'single_product.html', context)
    if staples_type == "sugar":
         product_type_name = "Masala Spices And Salt"
         single_pro_data = Staples_Product.objects.filter(category_Type_id=33)
         pro_data = Staples_Product.objects.filter(product_category_id=5)
         heading = "Sugar"
         context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                       'heading': heading,'no_of_item':no_of_item}
         return render(request, 'single_product.html', context)
    if staples_type == "jaggery":
         product_type_name = "Rice Products And Sugar"
         single_pro_data = Staples_Product.objects.filter(category_Type_id=34)
         pro_data = Staples_Product.objects.filter(product_category_id=5)
         heading = "Jaggery"
         context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                       'heading': heading,'no_of_item':no_of_item}
         return render(request, 'single_product.html', context)
        # end single rice products and sugar---------------------------------------------------------------------------------

    # start single dry fruits nuts and seeds -------------------------------------------------------------------------
    if staples_type == "cashew":
        product_type_name = "Dry Fruits,Nuts And Seeds"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=35)
        pro_data = Staples_Product.objects.filter(product_category_id=6)
        heading = "Cashew Nuts"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "almond":
        product_type_name = "Dry Fruits,Nuts And Seeds"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=36)
        pro_data = Staples_Product.objects.filter(product_category_id=6)
        heading = "Almonds"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "dates":
        product_type_name = "Dry Fruits,Nuts And Seeds"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=37)
        pro_data = Staples_Product.objects.filter(product_category_id=6)
        heading = "Dates And Raisins"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "dried":
        product_type_name = "Dry Fruits,Nuts And Seeds"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=38)
        pro_data = Staples_Product.objects.filter(product_category_id=6)
        heading = "Dried Fruits"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "edible":
        product_type_name = "Dry Fruits,Nuts And Seeds"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=39)
        pro_data = Staples_Product.objects.filter(product_category_id=6)
        heading = "Edible Seeds"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if staples_type == "othernut":
        product_type_name = "Dry Fruits,Nuts And Seeds"
        single_pro_data = Staples_Product.objects.filter(category_Type_id=40)
        pro_data = Staples_Product.objects.filter(product_category_id=6)
        heading = "Other Nuts"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # end single dry fruits nuts and seeds---------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------End single staples Product-------------------------------------
    # -----------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------Start single Snacks Product-------------------------------------
    # -----------------------------------------------------------------------------------------------------
    # start single Biscuits  -------------------------------------------------------------------------
    snacks_type = request.POST.get('snacks_type')
    if snacks_type == "cookies":
        product_type_name = "Biscuits"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=1)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Cookies"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "cream":
        product_type_name = "Biscuits"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=2)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Cream Biscuits"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "milk":
        product_type_name = "Biscuits"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=3)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Milk & Glucose"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "salted":
        product_type_name = "Biscuits"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=4)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Salted"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "cheeslets":
        product_type_name = "Biscuits"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=5)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Cheeslets"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "wafers_rusk":
        product_type_name = "Biscuits"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=6)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Wafers & Rusk"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)

    #ENd Biscuit--------------------------------------------------------------------------------
    #Start Chips,Namkeen & Snacks--------------------------------------------------------------------------------
    if snacks_type == "namkeen":
        product_type_name = "Chips,Namkeen & Snacks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=7)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        heading = "Namkeen"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "chips":
        product_type_name = "Chips,Namkeen & Snacks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=8)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        heading = "Chips"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "popcorn":
        product_type_name = "Chips,Namkeen & Snacks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=9)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        heading = "Popcorn, Paped & Fryums"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "snacky_nuts":
        product_type_name = "Chips,Namkeen & Snacks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=10)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        heading = "Snacky Nuts"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)

    # End Chips,Namkeen & Snacks--------------------------------------------------------------------------------
    # Start Tea and Coffee--------------------------------------------------------------------------------
    if snacks_type == "tea":
        product_type_name = "Tea And Coffee"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=11)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Tea"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "tea_bags":
        product_type_name = "Tea And Coffee"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=12)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Tea Bags"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "green_tea":
        product_type_name = "Tea And Coffee"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=13)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Green Tea"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "ice_tea":
        product_type_name = "Tea And Coffee"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=14)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Ice Tea"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "roast_ground":
        product_type_name = "Tea And Coffee"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=15)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Roast Ground"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "instant_coffee":
        product_type_name = "Tea And Coffee"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=16)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Instant Coffee"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # End Tea and Coffee--------------------------------------------------------------------------------
    # Start Juices--------------------------------------------------------------------------------
    if snacks_type == "mixed_fruit_juices":
        product_type_name = "Juices"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=17)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Mixed Fruit Juices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "guava_juices":
        product_type_name = "Juices"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=18)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Guava Juices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "orange_juices":
        product_type_name = "Juices"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=19)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Orange Juices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "lychee_juices":
        product_type_name = "Juices"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=20)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Lychee Juices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "apple_juices":
        product_type_name = "Juices"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=21)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Apple Juices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "fruit_drink":
        product_type_name = "Juices"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=22)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Fruit Drinks"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "other_juices":
        product_type_name = "Juices"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=23)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Other Juices"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)

    # End Juices--------------------------------------------------------------------------------
    # Start Soft & Health Drinks--------------------------------------------------------------------------------
    if snacks_type == "cold_drink":
        product_type_name = "Soft & Health Drinks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=24)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        heading = "Cold Drinks"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "energy_drinks":
        product_type_name = "Soft & Health Drinks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=25)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        heading = "Energy & Sports Drinks"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "non_alcoholic_drink":
        product_type_name = "Soft & Health Drinks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=26)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        heading = "Non Alcoholic Drinks"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "soda_tonic":
        product_type_name = "Soft & Health Drinks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=27)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        heading = "Soda & Tonic Water"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if snacks_type == "health_drink":
        product_type_name = "Soft & Health Drinks"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=28)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        heading = "Health Drink"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)

    # End Soft & Health Drinks--------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------
    # ---------------------------------------Start Single Snacks Product-------------------------------------
    # -----------------------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------------------------------------
    #----------------------------------------Start Packaged Food-------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------Breakfast Cereals--------------------------------------------------------
    packaged_type = request.POST.get('packaged_type')
    if packaged_type == "flake":
        product_type_name = "Breakfast Cereals"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=1)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Flakes"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "muesli":
        product_type_name = "Breakfast Cereals"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=2)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Muesli"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "oat":
        product_type_name = "Breakfast Cereals"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=3)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Oats"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "cereal":
        product_type_name = "Breakfast Cereals"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=4)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=1)
        heading = "Cereal Bars"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ----------------------------------------- End Breakfast Cereals---------------------------------------------------
    # ----------------------------------------- Noodles & Pasta---------------------------------------------------
    if packaged_type == "noodle":
        product_type_name = "Noodles & Pasta"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=5)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        heading = "Noodles"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "pasta":
        product_type_name = "Noodles & Pasta"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=6)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        heading = "Pasta"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "vermicelli":
        product_type_name = "Noodles & Pasta"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=7)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=2)
        heading = "Vermicelli"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # -----------------------------------------End Noodles & Pasta---------------------------------------------------
    # -----------------------------------------Start Ketchups & Spreads---------------------------------------------------
    if packaged_type == "ketchup":
        product_type_name = "Ketchups & Spreads"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=8)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Ketchups"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "dips":
        product_type_name = "Ketchups & Spreads"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=9)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Dips & Spreads"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "dressing":
        product_type_name = "Ketchups & Spreads"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=10)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=3)
        heading = "Dressing Sauce"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # -----------------------------------------End Ketchups & Spreads---------------------------------------------------
    # -----------------------------------------Start Chocolates & Sweets---------------------------------------------------
    if packaged_type == "chocolate":
        product_type_name = "Chocolates & Sweets"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=11)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Chocolates"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "sweet":
        product_type_name = "Chocolates & Sweets"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=12)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "sweets"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "candy":
        product_type_name = "Chocolates & Sweets"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=13)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Caandy & Gums"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "mouth":
        product_type_name = "Chocolates & Sweets"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=14)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Mouth Freshners"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "cake":
        product_type_name = "Chocolates & Sweets"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=15)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=4)
        heading = "Cake"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # --------------------------------------End Chocolates & Sweets---------------------------------------------------
    # --------------------------------------Start Jams & Honey---------------------------------------------------
    if packaged_type == "jam":
        product_type_name = "Jams & Honey"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=16)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        heading = "Jams"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "honey":
        product_type_name = "Jams & Honey"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=17)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=5)
        heading = "Honey"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # --------------------------------------End Jams & Honey---------------------------------------------------
    # --------------------------------------Start Pickles & Chutney---------------------------------------------------
    if packaged_type == "pickle":
        product_type_name = "Pickles & Chutney"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=18)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=6)
        heading = "Pickles"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "chutney":
        product_type_name = "Pickles & Chutney"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=18)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=6)
        heading = "Chutney"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # --------------------------------------End Pickles & Chutney---------------------------------------------------
    # --------------------------------------Start Ready To Cook--------------------------------------------------
    if packaged_type == "soup":
        product_type_name = "Ready To Cook"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=19)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=7)
        heading = "Soups"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "mixes":
        product_type_name = "Ready To Cook"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=19)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=7)
        heading = "Ready Mixes"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "meals":
        product_type_name = "Ready To Cook"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=20)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=7)
        heading = "Ready Meals"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # --------------------------------------End Ready To Cook--------------------------------------------------
    # --------------------------------------Start Cooking Sauces & Vineger--------------------------------------------------
    if packaged_type == "cooking":
        product_type_name = "Cooking Sauces & Vineger"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=21)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=8)
        heading = "Cooking Sauce"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if packaged_type == "vinegar":
        product_type_name = "Cooking Sauces & Vineger"
        single_pro_data = Snacks_Beverages_Product_Add.objects.filter(category_Type_id=22)
        pro_data = Snacks_Beverages_Product_Add.objects.filter(product_category_id=8)
        heading = "Vinegar"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)



    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------End Packaged Food---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------Start Personal & Baby Care---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    care_type = request.POST.get('care_type')
    # ---------------------------------------Soaps & Body Wash----------------------------------------------------------
    if care_type == "soaps":
        product_type_name = "Soaps & Body Wash"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=1)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Soaps"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "body_wash":
        product_type_name = "Soaps & Body Wash"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=2)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Body Wash"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "face_wash":
        product_type_name = "Soaps & Body Wash"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=3)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Face Wash"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "hand_wash":
        product_type_name = "Soaps & Body Wash"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=4)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Hand Wash"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "sanitizer":
        product_type_name = "Soaps & Body Wash"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=5)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Hand Sanitizer"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Soaps & Body Wash----------------------------------------------------------
    # ---------------------------------------Start hair_care----------------------------------------------------------

    if care_type == "shampoo":
        product_type_name = "Hair Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=6)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=2)
        heading = "Shampoo"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "conditioner":
        product_type_name = "Hair Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=7)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=2)
        heading = "Conditioner"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "hair_oil":
        product_type_name = "Hair Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=8)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=2)
        heading = "Hair Oil"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "hair_color":
        product_type_name = "Hair Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=9)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=2)
        heading = "Hair Color"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "hair_serum":
        product_type_name = "Hair Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=10)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=2)
        heading = "Hair Serum"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "styling_products":
        product_type_name = "Hair Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=11)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=2)
        heading = "Styling Products"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End hair_care----------------------------------------------------------
    # ---------------------------------------Start Oral Care----------------------------------------------------------
    if care_type == "toothpaste":
        product_type_name = "Oral Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=12)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Toothpaste"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "toothbrush":
        product_type_name = "Oral Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=13)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Toothbrush"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "mouthwash":
        product_type_name = "Oral Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=14)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Mouthwash"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "tougue_cleaners":
        product_type_name = "Oral Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=15)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Tongue Cleaners"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "floss":
        product_type_name = "Oral Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=16)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Floss"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Oral Care----------------------------------------------------------

    # ---------------------------------------Start Deos,Perfumes & Talc----------------------------------------------------------
    if care_type == "women_deo":
        product_type_name = "Deos,Perfumes & Talc"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=17)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=4)
        heading = "Women's Deo"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "men_deo":
        product_type_name = "Deos,Perfumes & Talc"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=18)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=4)
        heading = "Men's Deo"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "perfumes":
        product_type_name = "Deos,Perfumes & Talc"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=19)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=4)
        heading = "Perfumes"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "talc":
        product_type_name = "Deos,Perfumes & Talc"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=20)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=4)
        heading = "Talc"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)

    # ---------------------------------------End Deos,Perfumes & Talc----------------------------------------------------------

    # ---------------------------------------Start Creams,Lotions & Skin Care----------------------------------------------------------
    if care_type == "creams":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=21)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Creams"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "body_lotion":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=22)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Body Lotion"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "hair_removal":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=23)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Hair Removal"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "sunscreen":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=24)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Sunscreen"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "lip_care":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=25)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Lip Care"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "toner":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=26)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Toner"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "body_oil":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=27)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Body Oil"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "facepacks_scrubs":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=28)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Facepacks Scrubs"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "facial_tissues":
        product_type_name = "Creams,Lotions & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=29)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Facial Tissues"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Creams,Lotions & Skin Care----------------------------------------------------------

    # ---------------------------------------Start Diapers & Wipes----------------------------------------------------------
    if care_type == "diapers":
        product_type_name = "Diapers & Wipes"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=30)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=6)
        heading = "Diapers"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "wipes":
        product_type_name = "Diapers & Wipes"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=31)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=6)
        heading = "Wipes"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Diapers & Wipes----------------------------------------------------------

    # ---------------------------------------Start Kajal & Makeup----------------------------------------------------------
    if care_type == "kajal":
        product_type_name = "Kajal & Makeup"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=32)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Kajal"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "lipsticks":
        product_type_name = "Kajal & Makeup"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=33)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Lipsticks"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "makeup":
        product_type_name = "Kajal & Makeup"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=34)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Makeup"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "nail_care":
        product_type_name = "Kajal & Makeup"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=35)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Nail Care"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Kajal & Makeup----------------------------------------------------------

    # ---------------------------------------Start Welleness & Common Pharma----------------------------------------------------------
    if care_type == "sexual_welleness":
        product_type_name = "Welleness & Common Pharma"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=36)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=8)
        heading = "Sexual Welleness"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "cotton_bandages":
        product_type_name = "Welleness & Common Pharma"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=37)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=8)
        heading = "Cotton & Bandages"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "chwayanprash":
        product_type_name = "Welleness & Common Pharma"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=38)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=8)
        heading = "Chwayanprash"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "ointments":
        product_type_name = "Welleness & Common Pharma"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=39)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=8)
        heading = "Ointments"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "antiseptic":
        product_type_name = "Welleness & Common Pharma"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=40)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=8)
        heading = "Antiseptic"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "pain_relievers":
        product_type_name = "Welleness & Common Pharma"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=41)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=8)
        heading = "Pain Relievers"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "digestives":
        product_type_name = "Welleness & Common Pharma"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=42)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=8)
        heading = "Digestives"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Welleness & Common Pharma----------------------------------------------------------

    # ---------------------------------------Start Sanitary Needs----------------------------------------------------------
    if care_type == "sanitary_pads":
        product_type_name = "Sanitary Needs"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=43)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=9)
        heading = "Sanitary Pads"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "tampons":
        product_type_name = "Sanitary Needs"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=44)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=9)
        heading = "Tampons"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "initimate":
        product_type_name = "Sanitary Needs"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=45)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=9)
        heading = "Initimate Care"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Sanitary Needs----------------------------------------------------------

    # ---------------------------------------Start Shaving Needs----------------------------------------------------------
    if care_type == "blades_razors":
        product_type_name = "Shaving Needs"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=46)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=10)
        heading = "Blades & Razors"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "creams_foam":
        product_type_name = "Shaving Needs"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=47)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=10)
        heading = "Creams & Foam "
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "after_shave":
        product_type_name = "Shaving Needs"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=48)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=10)
        heading = "After Shave"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "shaving_brush":
        product_type_name = "Shaving Needs"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=49)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=10)
        heading = "Shaving Brush"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Shaving Needs----------------------------------------------------------

    # ---------------------------------------Start Baby Bath & Skin Care----------------------------------------------------------
    if care_type == "baby_soaps":
        product_type_name = "Baby Bath & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=50)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=11)
        heading = "Baby Soaps"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "baby_shampoo":
        product_type_name = "Baby Bath & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=51)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=11)
        heading = "Baby Shampoo"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "baby_oil":
        product_type_name = "Baby Bath & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=52)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=11)
        heading = "Baby Oil"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "baby_cream":
        product_type_name = "Baby Bath & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=53)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=11)
        heading = "Baby Cream"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "baby_powder":
        product_type_name = "Baby Bath & Skin Care"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=54)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=11)
        heading = "Baby Powder"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Baby Bath & Skin Care----------------------------------------------------------

    # ---------------------------------------Start Baby Food----------------------------------------------------------
    if care_type == "baby_cereal":
        product_type_name = "Baby Foods"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=55)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=12)
        heading = "Baby Cereal"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if care_type == "infant_formula":
        product_type_name = "Baby Foods"
        single_pro_data = Personal_Baby_care_Product_Add.objects.filter(category_Type_id=56)
        pro_data = Personal_Baby_care_Product_Add.objects.filter(product_category_id=12)
        heading = "Infant Formula"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Baby Food----------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------End Personal & Baby Care---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------Start Household Care---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    household_type = request.POST.get('household_type')
    # ---------------------------------------Start Detergents & Utensil Cleaners----------------------------------------------------------
    if household_type == "detergents":
        product_type_name = "Detergents & Utensil Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=1)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Detergents"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "fabric_care":
        product_type_name = "Detergents & Utensil Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=2)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Fabric Care"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "washing_bars":
        product_type_name = "Detergents & Utensil Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=3)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Washing Bars"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "dishwashe_liquid":
        product_type_name = "Detergents & Utensil Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=4)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Dishwashe Liquid"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "dishwash_bars":
        product_type_name = "Detergents & Utensil Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=5)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Dishwash Bars"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "scrub_pads":
        product_type_name = "Detergents & Utensil Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=6)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=1)
        heading = "Scrub Pads"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Detergents & Utensil Cleaners----------------------------------------------------------

    # ---------------------------------------Start Shoe Care----------------------------------------------------------
    if household_type == "shoe_polish":
        product_type_name = "Shoe Care"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=7)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=2)
        heading = "Shoe Polish"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Shoe Care----------------------------------------------------------

    # ---------------------------------------Start Floor & Other Cleaners----------------------------------------------------------
    if household_type == "toilet_cleaners":
        product_type_name = "Floor & Other Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=8)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Toilet Cleaners"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "floor_cleaners":
        product_type_name = "Floor & Other Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=9)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Floor Cleaners"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "kitchen_cleaner":
        product_type_name = "Floor & Other Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=10)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Kitchen Cleaners"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "drain_cleaner":
        product_type_name = "Floor & Other Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=11)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Drain Cleaners"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "cleaning_essentials":
        product_type_name = "Floor & Other Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=12)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Cleaning Essentials"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "glass_cleaners":
        product_type_name = "Floor & Other Cleaners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=13)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=3)
        heading = "Glass Cleaners"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Floor & Other Cleaners----------------------------------------------------------

    # ---------------------------------------Start Pet Food----------------------------------------------------------
    if household_type == "dog_food":
        product_type_name = "Pet Food"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=14)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=4)
        heading = "Dog Food"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "cat_food":
        product_type_name = "Pet Food"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=15)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=4)
        heading = "Cat Food"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Pet Food----------------------------------------------------------

    # ---------------------------------------Start Repellants & Freshners----------------------------------------------------------
    if household_type == "mosquito":
        product_type_name = "Repellants & Freshners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=16)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Mosquito Repellents"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "air":
        product_type_name = "Repellants & Freshners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=17)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Air Freshners"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "insectisides":
        product_type_name = "Repellants & Freshners"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=18)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=5)
        heading = "Insectisides"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Repellants & Freshners----------------------------------------------------------

    # ---------------------------------------Start Pooja Needs----------------------------------------------------------
    if household_type == "agarbatti":
        product_type_name = "Pooja Needs"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=19)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=6)
        heading = "Agarbatti & Dhoop"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "haven":
        product_type_name = "Pooja Needs"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=20)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=6)
        heading = "Haven Items"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "cotton":
        product_type_name = "Pooja Needs"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=21)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=6)
        heading = "Cotton Batti"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "daily_pooja":
        product_type_name = "Pooja Needs"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=22)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=6)
        heading = "Daily Pooja"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Pooja Needs----------------------------------------------------------

    # ---------------------------------------Start Paper & Disposables----------------------------------------------------------
    if household_type == "aluminium_foils":
        product_type_name = "Paper & Disposables"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=23)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Aluminium Foils"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "paper_napkins":
        product_type_name = "Paper & Disposables"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=24)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Paper Napkins"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "disposable_plates":
        product_type_name = "Paper & Disposables"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=25)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Disposable Plates & Utensils"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "kitchen_roll":
        product_type_name = "Paper & Disposables"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=26)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Kitchen Roll"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "toilet_paper":
        product_type_name = "Paper & Disposables"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=27)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Toilet Paper"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if household_type == "garbage_bags":
        product_type_name = "Paper & Disposables"
        single_pro_data = Household_care_Product_Add.objects.filter(category_Type_id=28)
        pro_data = Household_care_Product_Add.objects.filter(product_category_id=7)
        heading = "Garbage Bags"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ---------------------------------------End Paper & Disposables----------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------End Household Care---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------Start Dairy---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    dairy_type = request.POST.get('dairy_type')
    if dairy_type == "milk":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=1)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "Milk"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if dairy_type == "cheese":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=2)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "Cheese"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if dairy_type == "curd":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=3)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "Curd & Yogurts"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if dairy_type == "butter":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=4)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "Butter & Spreads"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if dairy_type == "soyamilk":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=5)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "Soya Milk"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if dairy_type == "buttermilk":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=6)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "ButterMilk & Lassi"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if dairy_type == "milkpowder":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=7)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "Milk Powder"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if dairy_type == "milkcream":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=8)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "Milk Cream"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    if dairy_type == "paneer":
        product_type_name = "Dairy"
        single_pro_data = Dairy_Product_Add.objects.filter(category_Type_id=9)
        pro_data = Dairy_Product_Add.objects.filter(product_category_id=1)
        heading = "Paneer & Tofu"
        context = {'single_pro_data': single_pro_data, 'pro_data': pro_data, 'product_type_name': product_type_name,
                   'heading': heading,'no_of_item':no_of_item}
        return render(request, 'single_product.html', context)
    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------End Dairy---------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------


























