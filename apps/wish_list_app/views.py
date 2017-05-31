from django.shortcuts import render, HttpResponse, redirect
from .models import User, Product, Wishlist
from django.contrib import messages

def main(request):
    # print(User._meta.db_table)### when create a raw query and not sure what the table name is , you can always find it by printing this line.
    # User.objects.all()[0].delete()
    # print
    # users = User.objects.all()
    # context = {
    #     'users': users
    # }

    return render(request, 'wish_list_app/index.html')

def regist(request):
    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

    postData = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'confirm': confirm,
    }

    model_resp = User.objects.reg_fn_validation(postData)
    if model_resp[0] == True:
        # print "User successfully created, should add flash message!"
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['first_name']
        # print "SESSION: "+ request.session['name']
        return redirect('/dashboard')
    else:
        for i in range(0, len(model_resp)):
            messages.warning(request, model_resp[i])
        return redirect('/')

def login(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    model_resp = User.objects.login_check(postData)
    if User.objects.login_check(postData) == True:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = User.objects.filter(email=postData['email'])[0].first_name
        return redirect('/dashboard')
    else:
        for i in range(0, len(model_resp)):
            messages.warning(request, model_resp[i])
        return redirect('/')

def dashboard(request):
    print 'LOGIN successfully'
    print 'USERS'
    for user in User.objects.all():
        print user
    print 'PRODUCTS'
    for product in Product.objects.all():
        print product
    print 'WISHES'
    for wish in Wishlist.objects.all():
        print wish
    context = {
        'name': request.session['name'],
        'my_wishes': Wishlist.objects.filter(user_id=request.session['id']),
        'products': Product.objects.exclude(wishes__user_id=request.session['id']),
    }
    return render(request, 'wish_list_app/wish_list.html', context)

def create(request):
    return render(request, 'wish_list_app/add.html')

def update(request):
    postData = {
        'item': request.POST['product'],
        'userID': request.session['id'],
    }
    errors = Product.objects.check_product(postData)
    if len(errors) == 0:
        return redirect('/dashboard')
    messages.info(request, errors[0])
    return redirect('/create')

def show(request, id):
    context = {
        'product': Product.objects.get(id=id),
        'users': User.objects.filter(wishes__product_id=id),
    }
    return render(request, 'wish_list_app/show.html', context)

def add(request, id):
    Wishlist.objects.create(user_id=request.session['id'], product_id=id)
    return redirect('/dashboard')

def remove(request, uID, pID):
    Wishlist.objects.get(user_id=uID, product_id=pID).delete()
    return redirect('/dashboard')

def delete(request, id):
    Product.objects.get(id=id).delete()
    return redirect('/dashboard')
