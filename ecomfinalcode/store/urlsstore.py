from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('signup/', views.signup, name="signup"),
	path('index/', views.index, name="index"),
	path('updateItem/', views.updateItem, name="updateItem"),
	path('processOrder/', views.processOrder, name="processOrder"),
	path('men/', views.men, name="men"),
	path('women/', views.women, name="women"),
	path('covid/', views.covid, name="covid"),
	path('other/', views.other, name="other"),
	path('main/', views.main, name="main"),
	
]