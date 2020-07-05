


from django.shortcuts import render, redirect
from django.urls import reverse

from store.forms import PersonForm

from django.contrib.auth.models import User

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from .utils import cookieCart,cartData,guestOrder
import json
import datetime

# Create your views here.

def store(request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']
            
      products = Product.objects.all()
      context = {'products':products, 'cartItems':cartItems, 'Person':Person}
      return render(request, 'store/store.html', context)

def cart(request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']

      context ={'items':items, 'order':order, 'cartItems':cartItems}
      return render(request, 'store/cart.html', context)


 
def checkout(request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']
            
            
      context ={'items':items, 'order':order, 'cartItems':cartItems}
      return render(request, 'store/checkout.html', context)

def signup(request):
      form= PersonForm(request.POST or None)
      if form.is_valid():
            form.save()
            return render(request, 'store/index.html')
      context= {'form': form }
        
      return render(request, 'store/signup.html', context)

      
def index(request):
      
      return render(request, 'store/index.html')


def updateItem(request):
      data = json.loads(request.body)
      productId = data['productId']
      action = data['action']
      print('Action:', action)
      print('Product:', productId)

      customer = request.user.customer
      product = Product.objects.get(id=productId)
      order, created = Order.objects.get_or_create(customer=customer, complete=False)

      orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

      if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
      elif action == 'remove':
             orderItem.quantity = (orderItem.quantity - 1)
      
      orderItem.save()
      if orderItem.quantity <=0:
            orderItem.delete()

      return JsonResponse('Item was added', safe=False)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt 
def processOrder(request):
      transaction_id = datetime.datetime.now().timestamp()
      data =json.loads(request.body)

      if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == order.get_cart_total:
                  order.complete =True
            order.save()
            ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)
      else:
            customer, order = guestOrder(request, data)
      total = float(data['form']['total'])
      order.transaction_id = transaction_id

      if total == order.get_cart_total:
            order.complete =True
      order.save()
      ShippingAddress.objects.create(
      customer=customer,
      order=order,
      address=data['shipping']['address'],
      city=data['shipping']['city'],
      state=data['shipping']['state'],
      zipcode=data['shipping']['zipcode'],
      )

      return JsonResponse('Payment completed', safe=False)

def men(request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']

      products = Product.objects.all()
      context = {'products':products,'cartItems':cartItems}
      return render(request, 'store/men.html', context)

def women(request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']

      products = Product.objects.all()
      context = {'products':products,'cartItems':cartItems}
      return render(request, 'store/women.html', context)

def covid(request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']

      products = Product.objects.all()
      context = {'products':products,'cartItems':cartItems}
      return render(request, 'store/covid.html', context)

def other(request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']

      products = Product.objects.all()
      context = {'products':products,'cartItems':cartItems}
      return render(request, 'store/other.html', context)

def main(requst):
      context = {'Person':Person}
      return render(request, 'store/main.html', context)

   




