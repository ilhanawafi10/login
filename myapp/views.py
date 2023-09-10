from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth, logout as logout_auth
# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email has already been used!')
            return redirect('login')
        
        #buatan akun pada user menggunakan perintah bawaan django
        user = User.objects.create_user(username=username, email=email, password=password)
        
        #menyimpan user
        user.save()
        
        #menjadikan user.is_active dan user.is_staff adalah false sebelum melakukan aktivasi akun
        user.is_active = False
        user.is_staff = False
        
        #melakukan generate token untuk aktivasi email
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        #membuat tautan aktivasi
        activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64':uid, 'token':token}))


        subject = 'Please activate your email'
        message = render_to_string('activation_email.html', {
            'user' : user,
            'activation_link' : activation_link
        })
        from_email = 'ilhanawafi10@gmail.com'
        recipient_list = [user.email]

        #mengirim email
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        messages.success(request, "Congratulations! your acoount has been created! Please activate your account!")


    return render(request, 'login.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.save()
        messages.success(request, 'Akun Anda berhasil diaktifkan. Silakan login.')
        return render(request, 'login.html')
    else:
        messages.error(request, 'Token aktivasi tidak valid atau sudah kadaluwarsa.')
        return (request, 'login.html')
    
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
    
        user = authenticate(request, username=username, password=password)
        
        if user is not None :
            if user.is_staff == True:
                login_auth(request, user)
                return HttpResponse('Berhasil Masuk')
            else :
                messages.warning(request, 'Please activate your account first!')
        else :
            messages.success(request, 'Your account was not found!')
            return redirect('login')
    
    return render(request, 'login.html')