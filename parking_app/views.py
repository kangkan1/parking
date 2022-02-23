from django.shortcuts import render, HttpResponse, redirect
from parking_app.models import Registration, PageViewsCounter, Employee, ContactUs
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

# demo user: demo@user.in, password: demouser123
# Create your views here.
def index(request):
    page = PageViewsCounter.objects.get(page_name='home')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save()

    #PageViewsCounter.objects.filter(page_name="home").update(counter=counter+1)
    return render(request, "index.html", {'rating_1':14, 'rating_2':17, 'rating_3':7, 'star_1':4.2, 'star_2':4.1, 'star_3':3.7})

def booking(request):
    page = PageViewsCounter.objects.get(page_name='booking')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save()
    if request.user.is_anonymous:
        #print("Anonymous user, from booking")
        return render(request, 'login.html', {'message':"Please login to continue"})
    elif request.user.is_authenticated:
        #print("request.user.username:"+request.user.username)
        return render(request, "booking.html")
           

def profile(request):
    page = PageViewsCounter.objects.get(page_name='profile')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save()
    if request.user.is_anonymous:
        #print("Anonymous user, from booking")
        return render(request, 'login.html', {'message':"Please login to continue"})
    elif request.user.is_authenticated:
        #print("request.user.username:"+request.user.username)
        user = request.user
        #print(f"user id: {user.id}")
        reg = Registration.objects.filter(user_id=user.id).order_by('date').reverse()[:5]
        reg_id = []
        date=[]
        start_time=[]
        ranged=[]
        price=[]
        payment=[]
        #print(len(reg))
        for i in range(5):
            if i<len(reg):
                #print(f"reg id: {reg[i].id}")
                reg_id.append(reg[i].id)
                date.append(reg[i].date)
                start_time.append(reg[i].start_time)
                ranged.append(f"{reg[i].ranged} hours")
                price.append(f"Rs. {reg[i].ranged*50}")
                if reg[i].payment:
                    payment.append("Done")
                else:
                    payment.append("Not Done")
            else:
                date.append('-')
                start_time.append('-')
                ranged.append('-')
                price.append('-')
                payment.append('-')    
        context={
            'reg_id':reg_id,
            'date':date,
            'start_time':start_time,
            'ranged':ranged,
            'price':price,
            'payment':payment
        }
        return render(request, "profile.html", context)

def login_user(request):
    if request.method == "POST":
        #print("POST method in login")
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print(f"email: {email}")
        #print(f"password: {password}")
        user = authenticate(username=email, password=password)
        if user is not None:
            #print("User authenticated")
            login(request, user)
            return redirect('/booking') 
        else:
            #print("Fake user") 
            context={
                "message":"Failed to login"
            } 
            return render(request, "login.html", context)
    page = PageViewsCounter.objects.get(page_name='login_user')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save()        
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    #print("USer logged out successfully")
    return redirect('/')

def signup(request):
    page = PageViewsCounter.objects.get(page_name='login_user')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save()  
    return render(request, "signup.html")

# this is for inbuild user
def create_user(request):
    if request.method == "POST":
        #print("post method in create user")
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print(f"password: {password}")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #check_user = User.objects.get(username=email)
  
        check_user = User.objects.filter(username=email)
        #print("User already exits")
        if check_user.exists():
            context={"message":"Email already in use"}
        else:       
            user = User.objects.create_user(username=email,
                                    email=email,
                                    password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            context={"created":"User created successfully"}
            
            #print("Django user created")
    return render(request, "signup.html", context)    


# this is for custom user
def create_account(request):
    if request.method == "POST":
        #print("post method")
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone = '+91'+request.POST.get('phone')
        check_email = User.objects.filter(email=email)
        check_phone = User.objects.filter(phone=phone)
        #print(check_email)
        #print(check_phone)
        context={"message":""}
        if check_email.exists():
            #print("User exits, email already taken")
            context={
                "message":"This email id: "+email+" is already in use"
            }
        elif check_phone.exists():
            #print("User exits, phone number already taken") 
            context={
                "message":"This phone number: "+phone+" is already in use"
            }   
        else:
            #print("Unique user")
            #print(f"email: {email} \npassword:{password} \nname: {name} \nphone: {phone}")
            user = User(email=email, password=password, name=name, phone=phone)
            user.save()
            #print("User created")
            context = {"created":"Your account was created successfully !"}
        
    return render(request, "signup.html", context)  


# book method will receive parameters from booking
def book(request):
    page = PageViewsCounter.objects.get(page_name='book')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save()  
    #print("book method called")
    current_user = request.user
    #print(f"user id: {current_user.id}")
    if request.method == "GET":
        #print("book get")
        return render(request, "booking.html")
    if request.method == "POST" and not request.user.is_anonymous:
        try:
            time = request.POST.get('time')
            ranged = request.POST.get('range')
            vehicle = request.POST.get('vehicle')
            date = request.POST.get('date')
        except: 
            a=a+1
            #print("some error occured")
        #print(f"time: {time}")
        #print(f"range: {ranged}")
        #print(f"vehicle: {vehicle}")
        #print(f"date: {date}")
        price = str(float(ranged)*50)
        id =current_user.id
        #print(f"current user id:{id}")
        #print(f"request.user.id: {request.user.id}")
        vehicle_type =''
        if vehicle == "Two Wheeler":
            vehicle_type='T'
        elif vehicle == "Four Wheeler": 
            vehicle_type='F'   
        elif  vehicle == "SUV":   
            vehicle_type='S' 
        reg = Registration(date=date, start_time=time,ranged=ranged, payment=False, vehicle=vehicle_type)
        reg.user_id = request.user
        reg.save()
        #print(f"reg.user_id: {reg.user_id}")
        #print(f"reg.id: {reg.id}")
        #print(f"price: {price}")
        #print(f"user id: {user_id}")
        context={
            'price':price,
            'ranged':ranged,
            'vehicle':vehicle,
            'date':date,
            'reg_id':reg.id
            }  
        #print(context) 
        #print("to be booked") 
        return render(request, "checkout.html", context)  
    return render(request, "checkout.html", context) 
    #return redirect('/checkout', kwargs=context) 

'''
redirect method
def foo(request):
    request.session['bar'] = 'FooBar'
    return redirect('app:view')

#jinja
{{ request.session.bar }}
'''

def checkout(request): 
    page = PageViewsCounter.objects.get(page_name='checkout')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save()
    if request.method == "POST" and not request.user.is_anonymous:
        id = request.POST.get('reg_id')
        reg = Registration.objects.get(id=id)
        reg.payment=True
        reg.save()
        #print(f"reg.user_id:{reg.user_id}")
        #print("POST request in checkout")
        price = request.POST.get('price')
        #print(f"reg_id: {id}")
        #print(f"reg.start_time: {reg.start_time}")
        #print(f"reg.ranged:{reg.ranged}")
        context={
            'booked_by':reg.user_id,
            'date':reg.date,
            'start_time':reg.start_time,
            'time_booked':reg.ranged,
            'price':reg.ranged*50,
            'payment':'Done'
        } 
        return render(request, "finalCheckout.html", context)
    if request.user.is_anonymous:
        return render(request, "login.html", {'message':'Please login to continue'})         
    return render(request, "checkout.html")


def final_checkout(request):
    page = PageViewsCounter.objects.get(page_name='final_checkout')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save()
    if request.user.is_anonymous:
        return render(request, "login.html", {'message':'Please login to continue'}) 
    return render(request, "finalCheckout.html")


def delete_booking(request):
    if request.method == "POST":
        #print("post method in delete_booking")
        check =request.POST.get('checkbox1')
        for i in range(1, 6, 1):
            #print(i)
            check =request.POST.get('checkbox'+str(i))
            #print(f"id: {check}")
            if check is not None and check.isnumeric():
                Registration.objects.filter(id=check).delete()
        #print(f"check: {check}")
    return redirect('/profile')    

def other_services(request):
    page = PageViewsCounter.objects.get(page_name='other_services')
    page.counter=page.counter+1
    page.save()
    total = PageViewsCounter.objects.get(page_name='total')
    total.counter = total.counter+1
    total.save() 
    return render(request, "other_services.html")

def emp_show(request):
    return redirect('/emp/show/0')

def employee_show(request, id):
    #print("id: "+id)
    i = int(id)
    multiplier=10
    #print("type of id: "+str(type(id)))
    employees = Employee.objects.all()[i*multiplier:multiplier*(i+1)]
    count = Employee.objects.all().count()
    return render(request, 'emp_show.html', {'employees':employees, 
                "count":count, "range":i, "next":(i+1), "prev":(i-1),
                "left":(multiplier*i), "right":(multiplier*(i+1))})
    
def employee_add(request):
    context = {}
    if request.method == "POST":
        #print("POST method: add employee")
        #emp_id = request.POST.get('employeeId')
        email = request.POST.get('email')
        emp_name = request.POST.get('name')
        emp_contact = request.POST.get('contact')
        emp_address = request.POST.get('address')
        #print("emp_id: "+emp_id)
        #print("name: "+request.POST.get('name'))
        #print("email: "+request.POST.get('email'))
        #print("contact: "+request.POST.get('contact'))
        check_id = Employee.objects.filter(eemail=email)
        #print("check_id: "+str(check_id.eid))
        if check_id.exists():
            context={"message":"Email or id is already in use"}
        elif len(emp_contact) != 10:
            context={"message":"Phone number should be of length 10"}   
        else:
            emp = Employee(eemail=email, ename=emp_name, econtact=emp_contact, eaddress=emp_address)
            emp.save()
            context={"created":"User created successfully"}   
        #context={"message":"Employee added successfully"}
    return render(request, 'emp_add.html', context)

def employee_delete(request, id):
    #print("emp delete id: "+id)
    try:
        Employee.objects.filter(eid=id).delete()
        #print("emp delete id: "+id)
    except:
        a=1    
    return redirect('/emp/show/0')

def employee_update(request, id):
    #print("Hello")
    emp =  Employee.objects.get(eid=id)
    #form = EmployeeForm(request.POST, instance = emp)
    message = ""
    created = ""
    if request.method == "POST":
        emp_id = request.POST.get('employeeId')
        email = request.POST.get('email')
        emp_name = request.POST.get('name')
        emp_contact = request.POST.get('contact')
        emp_address = request.POST.get('address')
        if len(emp_contact) != 10:
            message = "Phone number should be of length 10"
        elif len(emp_id) > 20:
            message = "Employee id should be of less than 20 characters"
        else:
            emp.eemail = email
            emp.ename = emp_name
            emp.econtact = emp_contact
            emp.address = emp_address
            emp.save()
            created ="Employee details updated successfully"
            return render(request, 'emp_update.html', {"emp":emp,"created":created, "message":message})
        #print("post method with id: "+id)
    context = {emp}
    return render(request, 'emp_update.html', {"emp":emp,"message":message,"created":created })

def techqueto_assignment(request):
    context = {'rating_1':14, 'rating_2':17, 'rating_3':7, 'star_1':4.2, 'star_2':4.1, 'star_3':3.7}
    return render(request, 'techqueto_assignment.html', context)


def saarthi_assignment(request):
    return render(request, 'saarthi_assignment.html')

def saarthi_assignment_action(request, st):
    return render(request, 'saarthi_assignment_action.html', {"action":st})

def contact_us_add(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        details = request.POST.get('details')
        if len(name) == 0 or len(email) == 0 or len(details) == 0:
            context = {"message":"Form can't be empty"}
        elif len(name) > 50:
            context = {"message":"Name can't be more than 50 character"}
        elif len(details) > 100:
            context = {"message":"Details can't be more than 100 character"}
        else:
            con = ContactUs(name=name, email=email, details = details)
            con.save()
            context={"created":"Information recorded successfully. We will get back ASAP"}    
    return render(request, 'contact_us_add.html', context)

def contact_us_show(request, id):
    i = int(id)
    multiplier=10
    #print("type of id: "+str(type(id)))
    show = ContactUs.objects.all()[i*multiplier:multiplier*(i+1)]
    count = ContactUs.objects.all().count()
    return render(request, 'contact_us_show.html', {'show':show, 
                "count":count, "range":i, "next":(i+1), "prev":(i-1),
                "left":(multiplier*i), "right":(multiplier*(i+1))})  
#error handling
def error_404(request, *args, **argv):
        data = {'error':'404'}
        return render(request,'error.html', data)

def error_500(request, *args, **argv):
        data = {'error':'500'}
        return render(request,'error.html', data)

def error_403(request,  exception):
        data = {'error':'403'}
        return render(request,'error.html', data)

def error_400(request,  exception):
        data = {'error':'400'}
        return render(request,'error.html', data)