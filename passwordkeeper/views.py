from django.shortcuts import render, redirect
from passwordkeeper.models import Password
from django.conf import settings
from cryptography.fernet import Fernet
from django.http import HttpResponseRedirect

# Create your views here

def get_cipher_suite():
    key = settings.PASSWORD_SECRET_KEY
    encoding = settings.ENCODING
    cipher_suite = Fernet(key.encode())
    return (cipher_suite, encoding,)

def encrypt_string(plain_text):
    cipher_suite, encoding = get_cipher_suite()
    encoded_text = cipher_suite.encrypt(plain_text.encode())
    return encoded_text.decode()

def decrypt_string(encoded_text):
    cipher_suite, encoding = get_cipher_suite()
    decoded_text = cipher_suite.decrypt(encoded_text.encode()).decode()
    return decoded_text

def index_view(request):
    password_list = Password.objects.all()
    return render(request, "index.html", context={'password_list': password_list})

def add_view(request):
    request_name = request.POST.get('inputName')
    request_pass = request.POST.get('inputPassword')
    Password.objects.create(
        name=request_name,
        password=encrypt_string(request_pass),
    )
    return redirect("/passwordkeeper/index")

def decrypt_password(request, id):
    password = Password.objects.get(id=id)
    decrypt_password = decrypt_string(password.password)
    password_list = Password.objects.all()
    return render(request, "index.html", context={'decrypt_password': decrypt_password, 'password_list': password_list})


    
