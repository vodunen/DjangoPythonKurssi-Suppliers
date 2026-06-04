from django.shortcuts import render, redirect
from .models import Supplier, Product, Customer, Order
from django.contrib.auth import authenticate, login, logout

# Loginpage
def loginview(request):
    return render (request, "loginpage.html")


# Login action
def login_action(request):
    user = request.POST['username']
    passw = request.POST['password']
    # Löytyykö kyseistä käyttäjää?
    user = authenticate(username = user, password = passw)
    #Jos löytyy:
    if user:
        # Kirjataan sisään
        login(request, user)
        # Tervehdystä varten context
        context = {'name': user.first_name}
        # Kutsutaan suoraan landingview.html
        return render(request,'landingpage.html',context)
    # Jos ei kyseistä käyttäjää löydy
    else:
        return render(request, 'loginerror.html')


# Logout action
def logout_action(request):
    logout(request)
    return render(request, 'loginpage.html')


# ==================== CUSTOMER VIEWS - ADDED ====================

# Customer list view
def customerlistview(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        customerlist = Customer.objects.all()
        context = {'customers': customerlist}
        return render (request,"customerlist.html",context)


# Add new customer
def addcustomer(request):
    a = request.POST['firstname']
    b = request.POST['lastname']
    c = request.POST['email']
    d = request.POST.get('phone', '')
    e = request.POST.get('address', '')
    f = request.POST.get('city', '')
    g = request.POST.get('country', 'Finland')
    
    Customer(firstname = a, lastname = b, email = c, phone = d, 
             address = e, city = f, country = g).save()
    return redirect(request.META['HTTP_REFERER'])


# Confirm delete customer
def confirmdeletecustomer(request, id):
    customer = Customer.objects.get(id = id)
    context = {'customer': customer}
    return render (request,"confirmdelcustomer.html",context)


# Delete customer
def deletecustomer(request, id):
    Customer.objects.get(id = id).delete()
    return redirect(customerlistview)


# ==================== ORDER VIEWS - ADDED ====================

# Order list view
def orderlistview(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        orderlist = Order.objects.all().order_by('-order_date')
        customerlist = Customer.objects.all()
        productlist = Product.objects.all()
        context = {'orders': orderlist, 'customers': customerlist, 'products': productlist}
        return render (request,"orderlist.html",context)


# Add new order
def addorder(request):
    a = request.POST['customer']
    b = request.POST['product']
    c = request.POST['quantity']
    d = request.POST.get('status', 'pending')
    e = request.POST.get('notes', '')
    
    Order(customer = Customer.objects.get(id = a), 
          product = Product.objects.get(id = b),
          quantity = c,
          status = d,
          notes = e).save()
    return redirect(request.META['HTTP_REFERER'])


# Confirm delete order
def confirmdeleteorder(request, id):
    order = Order.objects.get(id = id)
    context = {'order': order}
    return render (request,"confirmdelorder.html",context)


# Delete order
def deleteorder(request, id):
    Order.objects.get(id = id).delete()
    return redirect(orderlistview)


# ==================== OLD VIEWS ====================

# Product views
def productlistview(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        productlist = Product.objects.all()
        supplierlist = Supplier.objects.all()
        context = {'products': productlist, 'suppliers': supplierlist}
        return render (request,"productlist.html",context)

# Add new product
def addproduct(request):
    try:
        a = request.POST['productname']
        b = request.POST['packagesize']
        c = float(request.POST['unitprice'])
        d = int(request.POST['unitsinstock'])
        e = int(request.POST['supplier'])
        
        supplier = Supplier.objects.get(id=e)
        
        new_product = Product(
            productname = a, 
            packagesize = b, 
            unitprice = c, 
            unitsinstock = d, 
            supplier = supplier
        )
        new_product.save()
        
        print(f"✅ Product saved successfully: {a}")   # Success message
        
    except Exception as error:
        print(f"❌ Add product ERROR: {error}")   # Detailed error
        print("POST data was:", request.POST)     # Shows what was sent
    
    return redirect(request.META['HTTP_REFERER'])


def confirmdeleteproduct(request, id):
    product = Product.objects.get(id = id)
    context = {'product': product}
    return render (request,"confirmdelprod.html",context)


def deleteproduct(request, id):
    Product.objects.get(id = id).delete()
    return redirect(productlistview)


def edit_product_get(request, id):
        product = Product.objects.get(id = id)
        context = {'product': product}
        return render (request,"edit_product.html",context)


def edit_product_post(request, id):
        item = Product.objects.get(id = id)
        item.unitprice = request.POST['unitprice']
        item.unitsinstock = request.POST['unitsinstock']
        item.save()
        return redirect(productlistview)


def products_filtered(request, id):
    productlist = Product.objects.all()
    filteredproducts = productlist.filter(supplier = id)
    context = {'products': filteredproducts}
    return render (request,"productlist.html",context)



# Supplier views
def supplierlistview(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        supplierlist = Supplier.objects.all()
        context = {'suppliers': supplierlist}
        return render (request,"supplierlist.html",context)


def addsupplier(request):
    a = request.POST['companyname']
    b = request.POST['contactname']
    c = request.POST['address']
    d = request.POST['phone']
    e = request.POST['email']
    f = request.POST['country']
    Supplier(companyname = a, contactname = b, address = c, phone = d, email = e, country = f).save()
    return redirect(request.META['HTTP_REFERER'])


def searchsuppliers(request):
    search = request.POST['search']
    filtered = Supplier.objects.filter(companyname__icontains=search)
    context = {'suppliers': filtered}
    return render (request,"supplierlist.html",context)