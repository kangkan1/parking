from django.contrib import admin
from django.conf.urls import (
handler400, handler403, handler404, handler500,url 
)
#from django.conf.urls.defaults import patterns
from django.urls import path, include
from parking_app import views


urlpatterns = [
    path('', views.index, name='home'),
    path('booking', views.booking, name='Booking'),
    path('profile', views.profile, name='Profile'),
    path('login_user', views.login_user, name='Login user'),
    path('logout_user', views.logout_user, name='Logout'),
    path('signup', views.signup, name='Signup'),
    path('create_account', views.create_account, name='Create account'),
    path('create_user', views.create_user, name='Create user'),
    path('book', views.book, name='Book'),
    path('checkout', views.checkout, name='Checkout'),
    path('other_services', views.other_services, name='Other services'),
    path("final_checkout", views.final_checkout, name="Final Checkout"),
    path("delete_booking", views.delete_booking, name="Delete Booking"),

    path("techqueto_assignment", views.techqueto_assignment, name="Techqueto Assignment"),

    path("emp/show", views.emp_show, name="Employee Show"),
    path("emp/show/<str:id>", views.employee_show, name="Employee Show"),
    path("emp/add", views.employee_add, name="Employee Show"),
    path("emp/delete/<str:id>", views.employee_delete, name="Employee Delete"),
    path("emp/update/<str:id>", views.employee_update, name="Employee Update"),

    path("saarthi_assignment", views.saarthi_assignment, name="saarthi assignment"),
    path("saarthi_assignment_action/<str:st>/", views.saarthi_assignment_action, name="saarthi assignment action"),

    
    path("<str:id>", views.error_404, name="Error"),
    path("<str:id1>/<str:id2>", views.error_404, name="Error")

]
