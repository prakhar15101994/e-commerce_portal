# from app1.filters import ProductFilter

from django.db.models import Q
from app1.forms import CustomerProfileForm, CustomerRegisterForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django .views import View
from .models import*
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class ProductView(View):
    def get(self, request):
      
        totalitem=0
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        laptops=Product.objects.filter(category='laptop')

        # orders = Product.objects.all()
        # myFilter = ProductFilter(request.GET, queryset=orders)
        # orders = myFilter.qs
        
      
# ye if (totlitem) wala funcation kewal cart me kitna product hai dikhane k liye kiya gya ye hum kis bhijagah kar sakte hai
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        context={
            'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops, 'totalitem':totalitem
        }
        return render(request, 'home.html', context)

class ProductdetailView(View):
    def get(self, request, pk):
        products=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=products.id) & Q(user=request.user)).exists()
            return render(request, 'productdetail.html', {'products':products, 'item_already_in_cart':item_already_in_cart})
        else:
             return render(request, 'productdetail.html', {'products':products})

def mobileView(request, data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='redmi' or data=='samsung': 
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=7000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=7000)
    return render(request, 'mobile.html', {'mobiles':mobiles})

def TopWearView(request, data=None):
    if data==None:
        topwears=Product.objects.filter(category='TW')
    elif data=='Wrogn' or data=='Reebok' or data=='Zara' or data=='Lee': 
        topwears=Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        topwears=Product.objects.filter(category='TW').filter(discount_price__lt=500)
    
    elif data=='above':
        topwears=Product.objects.filter(category='TW').filter(discount_price__gt=500)
    return render(request, 'topwear.html', {'topwears':topwears})

def BottomWearView(request, data=None):
    if data==None:
        bottomwears=Product.objects.filter(category='BW')
    elif data=='Denim' or data=='PUMA' or data=='Flying_machine' or data=='RedTape': 
        bottomwears=Product.objects.filter(category='BW').filter(brand=data)
    elif data=='below':
        bottomwears=Product.objects.filter(category='BW').filter(discount_price__lt=1000)
    
    elif data=='above':
        bottomwears=Product.objects.filter(category='BW').filter(discount_price__gt=1000)
    return render(request, 'bottomwear.html', {'bottomwears':bottomwears})

class CustomerRegisterView(View):
    def get(self, request):
        form=CustomerRegisterForm()
        return render(request, 'customerregister.html', {'form':form})

    def post(self, request):
        form=CustomerRegisterForm(request.POST)
        username=request.POST['username']
        if form.is_valid():
            messages.success(request, f'congratulation!!!{username}..registered successfully')
            form.save()
        return render(request, 'customerregister.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form=CustomerProfileForm()
        return render(request, 'profile.html', {'form':form, 'active':'btn-primary'})
    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, f'congratulation!!!{name}.....registered successfully')
        return render(request, 'profile.html', {'form':form, 'active':'btn-primary'})

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add':add, 'active':'btn-primary'})


def add_to_cart(request):
    if request.user.is_authenticated:
        user=request.user
        product_id=request.GET.get('prod_id')
        product=Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart/')
    else:
        messages.warning(request, "Sorry you can not Add to Cart ..first Login here!")
        return redirect('/accounts/login/')
@login_required        
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discount_price)
                amount+=tempamount
                totalamount=amount+shipping_amount
            return render(request, 'add_to_cart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount} )
        else:
            return render(request, 'emptycart.html' )

@login_required  
def checkout_view(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discount_price)
            amount+=tempamount
        totalamount=amount+shipping_amount
    return render(request, 'checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})
@login_required  
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
       
    # yaha hame payment ke option redirect karana tha lekin abhi bad me karnge 
    return redirect("orders")
@login_required  
def order_done(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', {'order_placed':op})

def plus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        print("thi is product id ",prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70
        
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discount_price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount
                }
            return JsonResponse(data)
def minus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        # print("thi is product id ",prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70
        
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discount_price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount
                }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        # print("thi is product id ",prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
       
        c.delete()
        amount=0.0
        shipping_amount=70
        
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discount_price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount
            data={
                
                'amount':amount,
                'totalamount':totalamount
                }
            return JsonResponse(data)




  